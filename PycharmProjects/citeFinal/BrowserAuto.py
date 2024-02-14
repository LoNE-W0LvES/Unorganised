import asyncio
import os
from os import mkdir
from os.path import isdir
from time import sleep

import PySimpleGUI as Sg
from pyppeteer import launch
from pyppeteer.errors import TimeoutError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import visibility_of_element_located, presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait


def save_to_db(ref, worksheet, new_pos):
    bib = open(f"downloads\\scholar.bib", 'r').read().replace('\n', '\\n')
    end_note = open(f"downloads\\scholar.enw", 'r').read().replace('\n', '\\n')
    ref_man = open(f"downloads\\scholar.ris", 'r').read().replace('\n', '\\n')
    data = [ref, bib, end_note, ref_man]
    worksheet.insert_rows(row=new_pos, values=data, number=len(data))


def get_bib(refer, worksheet, position):
    val = []

    async def main_x():
        browser = await launch(args=['--window-size=1920,1080'], defaultViewport=None, headless=False)
        page = await browser.newPage()
        for ff in range(len(refer)):
            ref = refer['Reference'][ff]
            if not isdir(f"downloads"):
                mkdir(f"downloads")
            try:
                await page.goto('https://scholar.google.com/')
                await page.type('#gs_hdr_tsi', ref)
                await page.keyboard.press('Enter')
                # if ff == 0:
                #     sleep(50)
                await page.waitFor(500)
                await page.waitForSelector(
                    '#gs_res_ccl_mid > div > div.gs_ri > div.gs_fl.gs_flb > a.gs_or_cit.gs_or_btn.gs_nph > span',
                    {'timeout': 100000})
                await page.waitFor(500)
                await page.click('#gs_res_ccl_mid > div > div.gs_ri > div.gs_fl.gs_flb > a.gs_or_cit.gs_or_btn.gs_nph')
                await page.waitFor(2000)
                await page.waitForSelector('#gs_citi > a:nth-child(1)')
                await page.waitFor(500)
                download_path = os.getcwd() + f'.\\downloads'
                await page._client.send('Page.setDownloadBehavior', {
                    'behavior': 'allow',
                    'downloadPath': download_path
                })
                for x in range(3, 0, -1):
                    await page.waitFor(1000)
                    await page.click(f'#gs_citi > a:nth-child({x})')
                    if x == 1:
                        element = await page.waitForSelector('body > pre')
                        text = await (await element.getProperty('textContent')).jsonValue()
                        open(f"downloads\\scholar.bib", 'w').write(text)
                save_to_db(ref, worksheet, int(position) + ff)
            except TimeoutError:
                Sg.popup_error("Web element not found.")
                val.append(ff)
                break

        await page.close()
        await browser.close()

    asyncio.run(main_x())

    def selenium_run():
        def slow_type(element_: WebElement, texts: str):
            for character in texts:
                element_.send_keys(character)
                sleep(0.005)
            element_.send_keys(Keys.RETURN)

        firefox_options = webdriver.FirefoxOptions()
        download_path = os.getcwd() + f'\\downloads'
        firefox_options.set_preference("browser.download.folderList", 2)
        firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
        firefox_options.set_preference("browser.download.dir", download_path)
        firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
        browser = webdriver.Firefox(options=firefox_options)
        for ff in range(val[0], len(refer)):
            ref = refer['Reference'][ff]
            browser.get('https://scholar.google.com/')
            input_user = WebDriverWait(browser, 30).until(visibility_of_element_located((By.ID, "gs_hdr_tsi")))
            slow_type(input_user, ref)
            sleep(15)
            elem = browser.find_elements(By.CLASS_NAME, 'gs_or_svg')[1]
            elem.click()
            sleep(5)
            for x in range(3, 0, -1):
                sleep(1)
                browser.find_element(By.CSS_SELECTOR, f'#gs_citi > a:nth-child({x})').click()
                if x == 1:
                    element = WebDriverWait(browser, 10).until(
                        presence_of_element_located((By.CSS_SELECTOR, 'body > pre')))
                    text = element.get_attribute('textContent')
                    with open(f"downloads\\scholar.bib", 'w') as f:
                        f.write(text)
            save_to_db(ref, worksheet, int(position) + ff)

    if len(val) > 0:
        selenium_run()
