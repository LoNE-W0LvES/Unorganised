import asyncio
from pyppeteer import launch


async def main():
    chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    browser = await launch(args=['--window-size=1700,900'], headless=False, executablePath=chrome)
    page = await browser.newPage()
    await page.setViewport({'width': 1700, 'height': 900})
    await page.goto('https://www.facebook.com', {'waituntil': 'networkidle2', 'timeout': 0})
    print('loaded')
    await page.waitFor(1000)
    await page.goto('https://www.youtube.com', {'waituntil': 'networkidle2', 'timeout': 0})
    print('loaded')
    await page.waitFor(10000)


asyncio.get_event_loop().run_until_complete(main())
