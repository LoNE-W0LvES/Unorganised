const puppeteer = require('puppeteer');

(async ()=> {
    let username = 'nafi.mnrnafi.5'
    let password = 'i\'M lOne wOlVes'


    let browser = await puppeteer.launch({headless: false});
    const context = browser.defaultBrowserContext();
    await context.overridePermissions("https://www.facebook.com", ["geolocation", "notifications"]);
    let page = await browser.newPage();
    await page.goto("https://www.facebook.com");

    await page.type("#email", username);
    await page.type("#pass", password);
    await page.waitForTimeout(1000);
    await page.click("#u_0_2");
    await page.waitForTimeout(1000);
    await page.waitForSelector("#pagelet_composer");
    let content2 = await page.$$("#pagelet_composer");
})()