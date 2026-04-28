from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    def on_console(msg):
        print(f"Console [{msg.type}]: {msg.text}")
        
    page.on("console", on_console)
    page.on("pageerror", lambda err: print(f"Page Error: {err}"))
    
    print("Navigating...")
    page.goto('http://localhost:3000/')
    page.wait_for_timeout(3000)
    print("Done waiting.")
    browser.close()
