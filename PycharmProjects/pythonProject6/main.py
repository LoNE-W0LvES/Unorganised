from getpass import getuser
from os import getpid, path
from smtplib import SMTP_SSL
from ssl import create_default_context
from subprocess import call, Popen, PIPE
from threading import Thread
from time import sleep

import asyncio
from pyppeteer import launch

# ss = open('ss.txt', encoding="utf8").readlines()

from PyPDF2 import PdfReader

from os.path import isfile

if not isfile('./ref-data.txt'):
    open('ref-data.txt', 'w+')


def read_pdf(pdf):
    reader = PdfReader(pdf)
    str_x = []
    for i in reader.pages:
        try:
            text = i.extract_text()
            text = text.replace('\r', '').replace('\x81', '')
            str_x.append(text)
        except UnicodeEncodeError as e:
            print(e)

    ss = ' '.join(str_x).split('References')
    asyncio.get_event_loop().run_until_complete(main(ss[len(ss) - 1].replace('\n', ' ')))


async def main(pdf_name):
    chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    browser = await launch(args=['--window-size=1920,1080'], defaultViewport=None, headless=False, executablePath=chrome, userDataDir="C:\\Users\\nafim\\AppData\\Local\\Google\\Chrome\\User Data")
    page = await browser.newPage()
    await page.goto('https://chat.openai.com/', {'waituntil': 'networkidle2', 'timeout': 0})
    await page.type('#prompt-textarea', f'make a list without numbering using all these reference data {pdf_name}')
    # await page.keyboard.press('Enter')
    await page.click('#__next > div > div > div.overflow-hidden.w-full.h-full.relative.flex.z-0 > div > div > main > div > div.absolute.bottom-0.left-0.w-full.border-t.md\:border-t-0.dark\:border-white\/20.md\:border-transparent.md\:dark\:border-transparent.md\:bg-vert-light-gradient.bg-white.dark\:bg-gray-800.md\:\!bg-transparent.dark\:md\:bg-vert-dark-gradient.pt-2.md\:pl-2.md\:w-\[calc\(100\%-\.5rem\)\] > form > div > div.flex.w-full.items-center > div > button')
    await page.waitForFunction('document.querySelector("body").innerText.includes("Regenerate")', {'hidden': True, 'timeout': 9999999})

    await page.waitFor(5000)
    ht = await page.content()
    open('w.html', 'w+').write(str(ht))
    ref = '\n'.join(str(ht).split('<ul><li>')[1].split('</li></ul>')[0].replace('</p>', '').replace('</li>', '').replace('<li>', '').split('<p>')[1:])
    open('ref-data.txt', 'a').write(ref)
    await page.waitFor(5000)




