import os
import time
from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from .models import ExplorationRun, FeatureItem, ExplorationArtifact
from playwright.sync_api import sync_playwright

def get_stop_signal_key(run_id):
    return f"stop_exploration_{run_id}"

def stop_system_exploration(run_id):
    # Set cache signal
    cache.set(get_stop_signal_key(run_id), True, timeout=3600)
    # Create file signal just in case cache is unreliable
    stop_file = f"/tmp/{get_stop_signal_key(run_id)}"
    open(stop_file, 'w').close()

def is_stopped(run_id):
    if cache.get(get_stop_signal_key(run_id)):
        return True
    stop_file = f"/tmp/{get_stop_signal_key(run_id)}"
    if os.path.exists(stop_file):
        return True
    return False

@shared_task
def run_system_exploration(run_id):
    # Fix Django async unsafe error
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
    
    try:
        run = ExplorationRun.objects.get(id=run_id)
    except ExplorationRun.DoesNotExist:
        return
        
    run.status = 'running'
    run.start_time = timezone.now()
    run.save()
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            page = browser.new_page()
            
            # Simple traversal logic
            # Login
            page.goto('http://localhost:3000/login')
            page.fill('input[type="text"], input[name="username"]', 'admin')
            page.fill('input[type="password"], input[name="password"]', 'admin123')
            page.click('button[type="submit"]')
            page.wait_for_timeout(2000)
            
            # Check stop
            if is_stopped(run_id):
                raise Exception("Stopped by user")
            
            # Navigate to some areas and take screenshots
            areas = [
                {'url': 'http://localhost:3000/home', 'name': 'Home Dashboard', 'desc': 'Main landing page for the application'},
                {'url': 'http://localhost:3000/ai-intelligent-mode/projects', 'name': 'Workspace Management', 'desc': 'AI Intelligent Mode Workspace list'},
                {'url': 'http://localhost:3000/ai-intelligent-mode/testing', 'name': 'AI Testing Execution', 'desc': 'Execute AI Tests'},
            ]
            
            os.makedirs('/workspace/media/explorations', exist_ok=True)
            
            for idx, area in enumerate(areas):
                if is_stopped(run_id):
                    raise Exception("Stopped by user")
                    
                page.goto(area['url'])
                page.wait_for_timeout(3000)
                
                # Take screenshot
                filename = f"run_{run_id}_step_{idx}.png"
                filepath = f"/workspace/media/explorations/{filename}"
                page.screenshot(path=filepath)
                
                # Save feature item
                FeatureItem.objects.create(
                    run=run,
                    name=area['name'],
                    description=area['desc'],
                    url=area['url'],
                    screenshot_url=f"/media/explorations/{filename}"
                )
                
                # Also save as artifact
                ExplorationArtifact.objects.create(
                    run=run,
                    name=f"Screenshot: {area['name']}",
                    file_url=f"/media/explorations/{filename}",
                    artifact_type="screenshot"
                )
                
            browser.close()
            
            run.status = 'completed'
            run.end_time = timezone.now()
            run.result_summary = f"Successfully explored {len(areas)} features."
            run.save()
            
    except Exception as e:
        if str(e) == "Stopped by user":
            run.status = 'stopped'
            run.result_summary = "Exploration stopped by user."
        else:
            run.status = 'failed'
            run.result_summary = f"Error during exploration: {str(e)}"
        run.end_time = timezone.now()
        run.save()
