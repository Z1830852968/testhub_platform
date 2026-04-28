const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') {
      errors.push(`Console Error: ${msg.text()}`);
    }
  });
  
  page.on('pageerror', exception => {
    errors.push(`Uncaught Exception: ${exception}`);
  });

  await page.goto('http://localhost:3000/');
  await page.waitForTimeout(3000); // wait for vue to load

  if (errors.length > 0) {
    console.log("ERRORS FOUND:");
    console.log(errors.join('\n'));
  } else {
    console.log("No errors caught by playwright. Taking a snapshot of body...");
    const content = await page.content();
    console.log("Body length:", content.length);
    if (content.includes('id="app"')) {
        const appHtml = await page.$eval('#app', el => el.innerHTML);
        console.log("App HTML:", appHtml.substring(0, 200));
    }
  }

  await browser.close();
})();
