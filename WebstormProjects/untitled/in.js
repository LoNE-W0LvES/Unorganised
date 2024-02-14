const puppeteer = require('puppeteer');
const puppeteer_ex = require('puppeteer-extra')
const chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer_ex.use(StealthPlugin());

(async () => {
    const browser = await puppeteer.launch({ headless: false})
    const page = await browser.newPage()

    const navigationPromise = page.waitForNavigation()

    await page.goto('https://accounts.google.com/')

    await navigationPromise

    await page.waitForSelector('input[type="email"]')
    await page.click('input[type="email"]')

    await navigationPromise

    //TODO : change to your email
    await page.type('input[type="email"]', 'w3961500@gmail.com')

    await page.waitForSelector('#identifierNext')
    await page.click('#identifierNext')
    await page.waitForTimeout(5000);

    await page.waitForSelector('input[type="password"]')
    await page.click('input[type="email"]')


    //TODO : change to your password
    await page.type('input[type="password"]', 'yourpassword')

    await page.waitForSelector('#passwordNext')
    await page.click('#passwordNext')

    await navigationPromise

    //await browser.close()
})()