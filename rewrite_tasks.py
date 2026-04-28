import re

with open('apps/explorations/tasks.py', 'r') as f:
    content = f.read()

# We will just write a new tasks.py completely.

new_tasks_code = """
import os
import time
import json
from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from asgiref.sync import async_to_sync
from .models import ExplorationRun, FeatureItem, ExplorationArtifact
from apps.requirement_analysis.models import AIModelConfig
from apps.requirement_analysis.models import AIModelService
from playwright.sync_api import sync_playwright

def get_stop_signal_key(run_id):
    return f"stop_exploration_{run_id}"

def stop_system_exploration(run_id):
    cache.set(get_stop_signal_key(run_id), True, timeout=3600)
    stop_file = f"/tmp/{get_stop_signal_key(run_id)}"
    open(stop_file, 'w').close()

def is_stopped(run_id):
    if cache.get(get_stop_signal_key(run_id)):
        return True
    stop_file = f"/tmp/{get_stop_signal_key(run_id)}"
    if os.path.exists(stop_file):
        return True
    return False

JS_EXTRACT_DOM = '''
() => {
    let elements = document.querySelectorAll('a, button, input, [role="button"], [role="link"], .el-menu-item, .el-button');
    let interactiveElements = [];
    let idCounter = 1;
    
    elements.forEach(el => {
        // Skip hidden elements
        if (el.offsetWidth === 0 || el.offsetHeight === 0) return;
        
        let text = el.innerText || el.value || el.getAttribute('aria-label') || el.placeholder || '';
        text = text.trim().substring(0, 50);
        
        if (!text && el.tagName !== 'INPUT') return;
        
        let aiId = 'ai-id-' + idCounter++;
        el.setAttribute('data-ai-id', aiId);
        
        interactiveElements.push({
            id: aiId,
            tag: el.tagName.toLowerCase(),
            text: text,
            type: el.type || '',
            href: el.href || ''
        });
    });
    
    return interactiveElements;
}
'''

@shared_task
def run_system_exploration(run_id):
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'

    try:
        run = ExplorationRun.objects.get(id=run_id)
    except ExplorationRun.DoesNotExist:
        return

    run.status = 'running'
    run.start_time = timezone.now()
    run.save()

    # Get AI config
    model_config = AIModelConfig.objects.filter(role='explorer').first()
    if not model_config:
        model_config = AIModelConfig.objects.first()
    
    if not model_config:
        run.status = 'failed'
        run.result_summary = "没有找到任何可用的 AI 模型配置。请在配置中心添加 AI 网页探索专家配置。"
        run.end_time = timezone.now()
        run.save()
        return

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
            context = browser.new_context(viewport={'width': 1280, 'height': 800})
            page = context.new_page()

            base_url = run.base_url or 'http://localhost:3000'
            page.goto(base_url)
            page.wait_for_timeout(2000)

            if run.auth_type == 'form':
                # Try to perform form login
                username = run.auth_username or 'admin'
                password = run.auth_password or 'admin123'
                try:
                    page.fill('input[type="text"], input[name="username"]', username)
                    page.fill('input[type="password"], input[name="password"]', password)
                    page.click('button[type="submit"], .login-btn')
                    page.wait_for_timeout(3000)
                except Exception as e:
                    print(f"Auth form login failed: {e}")

            os.makedirs('/workspace/media/explorations', exist_ok=True)
            
            visited_urls = set()
            explored_features = 0

            for step in range(run.max_steps):
                if is_stopped(run_id):
                    raise Exception("Stopped by user")

                page.wait_for_load_state('networkidle', timeout=10000)
                page.wait_for_timeout(1000)
                current_url = page.url
                
                # Extract interactive elements
                elements = page.evaluate(JS_EXTRACT_DOM)
                
                # Build AI prompt
                prompt = f"你是一个专业的AI网页测试探索引擎。当前URL: {current_url}\\n"
                prompt += f"页面上可点击/交互的元素列表: {json.dumps(elements, ensure_ascii=False)}\\n"
                prompt += "请分析当前页面，提取出一个业务功能点，并决定下一步点击哪个元素进行探索。\\n"
                prompt += "要求：返回严格的JSON格式：\\n"
                prompt += "{\\n"
                prompt += "  \"feature_name\": \"提取的功能名称(如: 用户管理列表)\",\\n"
                prompt += "  \"description\": \"功能描述(如: 包含用户列表展示、搜索和添加按钮)\",\\n"
                prompt += "  \"next_action_id\": \"你决定下一步点击的元素ID(如: ai-id-1)\"\\n"
                prompt += "}"

                messages = [
                    {"role": "system", "content": "You are a smart QA web crawler."},
                    {"role": "user", "content": prompt}
                ]

                try:
                    ai_response = async_to_sync(AIModelService.call_openai_compatible_api)(model_config, messages)
                    content = ai_response.get('content', '{}')
                    
                    # Clean markdown code blocks if any
                    content = content.replace("```json", "").replace("```", "").strip()
                    decision = json.loads(content)
                    
                    feature_name = decision.get('feature_name', f"Feature at {current_url}")
                    description = decision.get('description', "Auto discovered feature")
                    next_id = decision.get('next_action_id')
                    
                    # Take screenshot
                    filename = f"run_{run_id}_step_{step}.png"
                    filepath = f"/workspace/media/explorations/{filename}"
                    page.screenshot(path=filepath)

                    # Save feature item
                    FeatureItem.objects.create(
                        run=run,
                        name=feature_name,
                        description=description,
                        url=current_url,
                        screenshot_url=f"/media/explorations/{filename}"
                    )

                    ExplorationArtifact.objects.create(
                        run=run,
                        name=f"截图: {feature_name}",
                        file_url=f"/media/explorations/{filename}",
                        artifact_type="screenshot"
                    )
                    explored_features += 1

                    # Execute click
                    if next_id:
                        selector = f"[data-ai-id='{next_id}']"
                        if page.locator(selector).count() > 0:
                            page.click(selector, timeout=3000)
                        else:
                            # Try to click a random link if AI hallucinated
                            links = page.locator("a").all()
                            if links:
                                links[0].click()
                    else:
                        break # AI decided not to click

                except Exception as e:
                    print(f"AI Exploration Step Error: {e}")
                    # If AI fails, fallback to naive click
                    links = page.locator("a, .el-menu-item").all()
                    if links:
                        try:
                            links[step % len(links)].click()
                        except:
                            pass

            browser.close()

            run.status = 'completed'
            run.end_time = timezone.now()
            run.result_summary = f"成功探索完毕，提取了 {explored_features} 个业务功能点。"
            run.save()

    except Exception as e:
        if str(e) == "Stopped by user":
            run.status = 'stopped'
            run.result_summary = "探索已被用户手动终止。"
        else:
            run.status = 'failed'
            run.result_summary = f"探索过程中发生错误: {str(e)}"
        run.end_time = timezone.now()
        run.save()

"""

with open('apps/explorations/tasks.py', 'w') as f:
    f.write(new_tasks_code)

