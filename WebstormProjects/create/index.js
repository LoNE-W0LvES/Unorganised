const fs = require('fs');
const path = require('path');
const crypto = require("crypto");
const process = require('process');
const puppeteer = require('puppeteer');
const extractUrls = require("extract-urls");
const puppeteer_ex = require('puppeteer-extra')
const Adblock = require('puppeteer-extra-plugin-adblocker')
const StealthPlugin = require('puppeteer-extra-plugin-stealth')
puppeteer_ex.use(Adblock())
puppeteer_ex.use(StealthPlugin())

const chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const BASE_URL1 = 'https://fruitlab.com/login';
const BASE_URL5 = 'https://www.gmailnator.com';
const BASE_URL3 = 'https://fruitlab.com/juice';
const BASE_URL2 = 'https://www.gmailnator.com/inbox/#';
const BASE_URL0 = 'https://fruitlab.com/user-register';
const BASE_URL4 = 'https://fruitlab.com/create-chat-account';
const MALE = 'gemale019IAM23RT';
const FEMALE = 'gefemale019IAM23';

let i;
let security = [];
let consoleInputs=[];
const date_x = new Date();
process.argv.forEach(function(value, index, array){consoleInputs=array});
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
    let var7 = args[5]
    security.push(crypto.createHash('md5').update(var1 + var0 + var2 + var6 + var4 + var5 + var3 + var7).digest('hex'));
}
if (security.includes(args[0]) === false) {process.exit(1)}
if (security.includes(args[0]) === false) {process.exit(1)}

(async ()=>{
    console.log('Opening browser');
    const browser = await puppeteer.launch({args: ['--window-size=915,900'],headless:(args[1] === 'false'),executablePath: chrome});
    const page = await browser.newPage();
    await page.setViewport({ width: 900, height: 900 })
    console.log('Making email');
    await page.goto(BASE_URL5);
    await page.waitForTimeout(15000);
    await page.waitForSelector('button[id="button_go"]')
    await page.waitForTimeout(1000);
    await page.click('button[id="button_go"]', {clickCount: 1});
    await page.waitForTimeout(5000);
    const url = page.url();
    let gmail = url.replace('https://www.gmailnator.com/inbox/#', '').replace('/', '').toString()
    console.log('New Mail: '+ gmail);

    console.log('Writing email to file');
    fs.appendFile('./Essentials/credentials.csv', "\n"+gmail, (err) => {if (err) throw err})
    await page.waitForTimeout(1000);
    console.log('Writing password to file');
    fs.appendFile('./Essentials/credentials.csv', ","+args[5], (err) => {if (err) throw err})
    await page.waitForTimeout(1000);
    console.log('Writing vpn to file');
    fs.appendFile('./Essentials/credentials.csv', ","+args[6], (err) => {if (err) throw err});
    await page.waitForTimeout(1000);
    console.log('Opening Fruitlab page');
    await page.goto(BASE_URL0,{waituntil:'networkidle2', timeout: 0});
    await page.waitForTimeout(1000);
    console.log('Gender: '+ args[2].trim());
    if (args[2].trim()==='male'){await page.select('select[name="gender_select"]',MALE)}
    else {await page.select('select[name="gender_select"]',FEMALE)}
    console.log('First Name: '+ args[3]);
    await page.type('input[name="firstName"]',args[3],{delay:50});
    console.log('Last Name: '+ args[4]);
    await page.type('input[name="lastName"]',args[4],{delay:50});
    let display_name = args[3]+'_'+args[4]+(Math.floor(Math.random() * (100 - 10 + 1) + 10)).toString()
    console.log('Display Name: '+ display_name);
    await page.type('input[name="signup_username"]',display_name,{delay:50});
    await page.waitForTimeout(100);
    let day = (Math.floor(Math.random() * (30 - 1 + 1) + 1)).toString()
    console.log('Birth Date: '+ day);
    await page.select('select[name="day_select"]',day);
    await page.waitForTimeout(100);
    let month = (Math.floor(Math.random() * (12 - 1 + 1) + 1)).toString()
    console.log('Birth Month: '+ month);
    await page.select('select[name="month_select"]',month);
    await page.waitForTimeout(100);
    let Year = (Math.floor(Math.random() * (2002 - 1995 + 1) + 1995)).toString()
    console.log('Birth Year: '+ Year);
    await page.select('select[name="year_select"]',Year);
    console.log('Email: ' + gmail);
    await page.type('input[name="signup_email"]',gmail,{delay:50});
    console.log('Password: ' + args[5]);
    await page.type('input[name="signup_password"]',args[5],{delay:50});
    console.log('Confirm Password: ' + args[5]);
    await page.type('input[name="conf_password"]',args[5],{delay:50});
    console.log('Agreeing Terms');
    await page.click("#signup_terms", {clickCount: 1});
    await page.click("#signup-terms-communication", {clickCount:1});
    await page.waitForTimeout(5000);
    console.log('Creating Account');
    let CreateAccountButton=await page.$x('//button[contains(text(),"CREATE ACCOUNT")]');
    await CreateAccountButton[0].click();
    //click confirmation
    console.log('Confirming Gmail');
    await page.waitForTimeout(12000);
    await page.goto(BASE_URL2+gmail,{waituntil:'networkidle2', timeout: 0});
    let fruit_found=false;
    console.log('Looking for email');
    while (fruit_found===false){
        console.log('Waiting . . . ');
        await page.reload({ waitUntil: ["networkidle2", "domcontentloaded"] });
        await page.waitForTimeout(5000);
        let fruit_lookup=await page.$x('//td[contains(text(),"Fruitlab")]');
        if (fruit_lookup.length !== 0){fruit_found=true}
    }
    console.log('Email found');
    console.log('Confirming');
    const cdp = await page.target().createCDPSession();
    const entries = Object.values(await cdp.send('Page.captureSnapshot', { format: 'mhtml' }));
    let urls1 = extractUrls(entries[0].replace(/(\r\n|\n|\r)/gm, ""))
    console.log('Getting mail');

    for (i = 0; i <urls1.length; i++) {
        if (urls1[i].includes('messageid')){
            let test_x = urls1[i].replace('=', '')
            await page.goto(test_x,{waituntil:'networkidle2', timeout: 0});
            await page.waitForTimeout(5000);
            const mail_box = Object.values(await cdp.send('Page.captureSnapshot', { format: 'mhtml' }));
            let content = mail_box[0].replace(/(\r\n|\n|\r)/gm, "")
            if (content.includes('fruitlab') || content.includes('fruitlab')){
                let links = content.split('3D"')
                for (i = 0; i <links.length; i++){
                    let verify_link = links[i]
                    if (verify_link.includes('fruitlab.com/user_email_verified')){
                        let link_clean = verify_link.replace(/(=)/gm, '').replace('tst3D', 'tst=') + '='
                        await page.goto(link_clean,{waituntil:'networkidle2', timeout: 0})
                    }
                }
            }
        }
    }

    await page.waitForTimeout(5000);
    console.log('Logging in');
    await page.goto(BASE_URL1,{waituntil:'networkidle2', timeout: 0});
    await page.waitForTimeout(1000);
    console.log('Username :' + gmail);
    await page.type('input[name="login_username"]',gmail,{delay:50});
    console.log('Password :' + args[5]);
    await page.type('input[name="login_password"]',args[5],{delay:50});
    console.log('Signing in');
    let loginButton=await page.$x('//button[contains(text(),"SIGN IN")]');
    await loginButton[0].click();
    await page.waitForTimeout(8000);
    console.log('Opening Juice for first time!!');
    await page.goto(BASE_URL3,{waituntil:'networkidle2', timeout: 0});
    await page.waitForTimeout(2000);
    try {await page.goto(BASE_URL4)} catch (e) {}
    console.log('Closing');
    await browser.close()
})()
