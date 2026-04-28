import sys
import asyncio
from playwright.async_api import async_playwright

async def run_smoke_test(url):
    print(f"Starting smoke test for frontend route: {url}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        errors = []
        page.on("pageerror", lambda err: errors.append(err.message))
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

        try:
            # Go to the route
            response = await page.goto(url, wait_until="networkidle")
            
            if not response or not response.ok:
                print(f"❌ Failed to load page. Status: {response.status if response else 'Unknown'}")
                sys.exit(1)
                
            # Check if there is an element that indicates the app loaded
            # E.g., #app, or some title
            await page.wait_for_selector("#app", timeout=5000)
            
            # Additional check: let's wait a bit to see if any console errors show up
            await page.wait_for_timeout(2000)
            
            # Filter out non-critical errors if necessary, but generally we want to catch big ones.
            # E.g., Vue warnings or unhandled rejections.
            critical_errors = [e for e in errors if "ERR_CONNECTION_REFUSED" in e or "Failed to load resource" in e or "TypeError" in e]
            
            if critical_errors:
                print(f"❌ Smoke test failed! Critical errors found:")
                for e in critical_errors:
                    print(f"  - {e}")
                sys.exit(1)
            else:
                print(f"✅ Smoke test passed! Page {url} loaded successfully.")
                
        except Exception as e:
            print(f"❌ Smoke test failed with exception: {e}")
            sys.exit(1)
        finally:
            await browser.close()

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5173/ai-intelligent-mode/projects"
    asyncio.run(run_smoke_test(url))
