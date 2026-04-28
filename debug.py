from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    errors = []
    
    def handle_console(msg):
        if msg.type == 'error':
            errors.append(msg.text)
            
    page.on("console", handle_console)
    page.on("pageerror", lambda err: errors.append(str(err)))
    
    page.goto('http://localhost:3000/')
    page.wait_for_timeout(3000)
    
    if errors:
        print("ERRORS FOUND:")
        for err in errors:
            print(err)
    else:
        app_html = page.evaluate("document.getElementById('app').innerHTML")
        print("App HTML:", app_html[:200])
        
    browser.close()
