const path = require('path');
const crypto = require("crypto");
const process = require('process');
const puppeteer = require('puppeteer');
const chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const BASE_URL_0 = 'https://www.facebook.com';

let i;
let security = [];
let consoleInputs=[];
const date_x = new Date();
process.argv.forEach(function(value, index, array) {consoleInputs=array});
let args = new Buffer.from(consoleInputs[2], 'base64').toString('ascii').split(',.,');

for(i=0;i<60;i++){
    let copiedDate = new Date(date_x.getTime());
    copiedDate.setSeconds(copiedDate.getSeconds() - i);
    let var0 = process.env['USERPROFILE'].split(path.sep)[2]
    let var1 = (copiedDate.getMonth() + 1).toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false}).toString()
    let var2 = copiedDate.getDate().toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false}).toString()
    let var3 = copiedDate.getFullYear().toLocaleString('en-US', {minimumIntegerDigits: 4, useGrouping: false}).toString()
    let var4 = copiedDate.getHours().toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false}).toString()
    let var5 = copiedDate.getMinutes().toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false}).toString()
    let var6 = copiedDate.getSeconds().toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false}).toString()
    let var7 = args[3]
    security.push(crypto.createHash('md5').update(var7 + var6 + var5 + var4 + var3 + var2 + var1 + var0).digest('hex'));
}
if (security.includes(args[0]) === false) {process.exit(1)}
if (security.includes(args[0]) === false) {process.exit(1)}
if (security.includes(args[0]) === false) {process.exit(1)}

(async ()=>{
    let page_urls = args[5].split('(^_^)')

    //open chrome

    const browser = await puppeteer.launch({args: ['--window-size=1700,900'],headless: (args[1] === 'false'),executablePath: chrome});
    const context = browser.defaultBrowserContext();
    await context.overridePermissions("https://www.facebook.com", ["geolocation", "notifications"]);
    const page = await browser.newPage();
    await page.setViewport({ width: 1700, height: 900 });

    await page.goto(BASE_URL_0,{waituntil:'networkidle2', timeout: 0});
    await page.waitForTimeout(1000);

    await page.waitForSelector('button[name="login"]');
    await page.type('input[name="email"]', args[2], {delay: 60});
    await page.type('input[name="pass"]', args[3], {delay: 50});
    try {
        await page.click('button[name="login"]');
    } catch (error){}
    try {
        await page.click('button[type="submit"]');
    } catch (error){}

    await page.waitForTimeout(5000);

    for (let url of page_urls) {
        try {
            await page.goto(url,{waituntil:'networkidle2', timeout: 0});
            await page.waitForSelector('div[class="m9osqain a5q79mjw gy2v8mqq jm1wdb64 k4urcfbm qv66sw1b"]');
            await page.click('div[class="m9osqain a5q79mjw gy2v8mqq jm1wdb64 k4urcfbm qv66sw1b"]');
            await page.waitForTimeout(5000);
            await page.click('div[class="gcieejh5 bn081pho humdl8nn izx4hr6d rq0escxv oo9gr5id t5a262vz o0t2es00 b1v8xokw datstx6m f530mmz5 lzcic4wl ecm0bbzt rz4wbd8a sj5x9vvc a8nywdso k4urcfbm o8yuz56k"]');
            await page.waitForTimeout(5000);
            await page.type('div[class="gcieejh5 bn081pho humdl8nn izx4hr6d rq0escxv oo9gr5id t5a262vz o0t2es00 b1v8xokw datstx6m f530mmz5 lzcic4wl ecm0bbzt rz4wbd8a sj5x9vvc a8nywdso k4urcfbm o8yuz56k"]', args[4], {delay: 50});
            await page.waitForTimeout(25000);
            await page.click('div[aria-label="Post"]');
            await page.waitForTimeout(25000);
        } catch (error){}

    }
    await page.waitForTimeout(5000);
    await browser.close();
})()