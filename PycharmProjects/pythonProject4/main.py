from getpass import getuser
from os import getpid, path
from smtplib import SMTP_SSL
from ssl import create_default_context
from subprocess import call, Popen, PIPE
from threading import Thread
from time import sleep

import asyncio
from pyppeteer import launch

ss = open('ss.txt', encoding="utf8").readlines()


async def main():
    chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    browser = await launch(args=['--window-size=1920,1080'], defaultViewport=None, headless=False,
                           executablePath=chrome,
                           userDataDir="C:\\Users\\nafim\\AppData\\Local\\Google\\Chrome\\User Data")
    page = await browser.newPage()
    for ff in range(len(ss)):
        await page.goto('https://scholar.google.com/')
        await page.type('#gs_hdr_tsi', ss[ff])
        await page.keyboard.press('Enter')
        # if ff == 0:
        #     sleep(50)
        await page.waitFor(500)
        await page.waitForSelector('#gs_res_ccl_mid > div > div.gs_ri > div.gs_fl.gs_flb > a.gs_or_cit.gs_or_btn.gs_nph > span')
        await page.waitFor(500)
        await page.click('#gs_res_ccl_mid > div > div.gs_ri > div.gs_fl.gs_flb > a.gs_or_cit.gs_or_btn.gs_nph')
        await page.waitFor(2000)
        await page.waitForSelector('#gs_citi > a:nth-child(1)')
        await page.waitFor(500)
        await page.click('#gs_citi > a:nth-child(1)')
        await page.waitFor(500)
        element = await page.waitForSelector('body > pre')
        text = await (await element.getProperty('textContent')).jsonValue()
        open('bib.txt', 'a').write(text)


asyncio.get_event_loop().run_until_complete(main())