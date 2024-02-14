# name_list = open('gg.csv', 'r').read().split('\n')[1:]
#
# name_list_2 = []
# for i in name_list:
#     name_list_2.append(i.split(','))
#
# print(name_list_2)
#
# for k in range(len(name_list_2)):
#     name_list_2[k] = ','.join(name_list_2[k])
#
# print(name_list_2)

import asyncio
from pyppeteer import launch


async def main():
    chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    browser = await launch(args=['--window-size=1920,1080'], defaultViewport=None, headless=False, executablePath=chrome, userDataDir="C:\\Users\\nafim\\AppData\\Local\\Google\\Chrome\\User Data")
    page = await browser.newPage()
    await page.goto('https://tncentral.ncc.unesp.br/tnC_search.html', {'waituntil': 'networkidle2', 'timeout': 1000})
    await page.type('body > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(1) > fieldset > table > tbody > tr:nth-child(4) > td:nth-child(2) > input', 'TnMERI1_p')
    await page.click('body > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(1) > fieldset > table > tbody > tr:nth-child(16) > td:nth-child(2) > input:nth-child(1)')
    # await page.waitForFunction('document.querySelector("body").innerText.includes("page")', {'hidden': True, 'timeout': 9999999})
    # ht = str(await page.content()).split('<td></td></tr></tbody></table></td><td')[1].split('</tbody></table>')[0].split('</td></tr>')[0].split('</td><td valign="top">')[3]
    # ht = str(await page.content()).split('</tbody></table>')
    # tab_3 = ''
    # new_arr = [m.replace('\n', '').replace('<font color="red">', '').replace('</font>', '').replace('</td></tr><tr',
    #                                                                                                 '</td><td valign="top">').split(
    #     '</td><td valign="top">')[1:9] for m in ht if '</td><td valign="top">' in m.lower()]
    # print(new_arr)
    # for k in range(len(new_arr)):
    #     if new_arr[k][0].lower() == 'TnXorYNA12'.lower():
    #         tab_3 = new_arr[j][3]
    #         break
    #
    # name_list_2[j][2] = tab_3
    # print(name_list_2[j])
    # await page.waitFor(1000)
    ht = str(await page.content())
    open('w.html', 'w+').write(ht)

asyncio.get_event_loop().run_until_complete(main())
