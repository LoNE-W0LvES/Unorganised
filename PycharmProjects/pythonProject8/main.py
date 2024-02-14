import asyncio
from pyppeteer import launch

# ss = open('ss.txt', encoding="utf8").readlines()

from os.path import isfile
op = open('ttxd.csv', 'r').read().split('\n')
name_list = op[1:]


name_list_2 = []
for i in name_list:
    name_list_2.append(i.split(','))


async def main():
    chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    browser = await launch(args=['--window-size=1920,1080'], defaultViewport=None, headless=True,
                           executablePath=chrome,
                           userDataDir="C:\\Users\\nafim\\AppData\\Local\\Google\\Chrome\\User Data")
    page = await browser.newPage()
    for j in range(len(name_list_2)):
        if name_list[j] != '':
            print(j)
            await page.goto('https://tncentral.ncc.unesp.br/tnC_search.html',
                            {'waituntil': 'networkidle2', 'timeout': 10000})
            await page.waitFor(500)
            await page.type(
                'body > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(1) > fieldset > table > tbody > tr:nth-child(4) > td:nth-child(2) > input',
                name_list_2[j][0])
            await page.click(
                'body > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(1) > fieldset > table > tbody > tr:nth-child(16) > td:nth-child(2) > input:nth-child(1)')

            await page.waitFor(1500)
            ht = str(await page.content())
            if 'Not found.' not in ht:
                tab_3 = ''
                htm = ht.split('</tbody></table>')
                new_arr = [m.replace('\n', '').replace('<font color="red">', '').replace('</font>', '').replace('</td></tr><tr',
                                                                                                                '</td><td valign="top">').split(
                    '</td><td valign="top">')[1:9] for m in htm if '</td><td valign="top">' in m.lower()]
                for k in range(len(new_arr)):
                    if new_arr[k][0].lower() == name_list_2[j][0].lower():
                        tab_3 = new_arr[k][3]
                        break

                name_list_2[j][2] = tab_3
            else:
                name_list_2[j][2] = ''
            op.pop(1)
            await page.waitFor(1000)
            open('w.txt', 'a').write(','.join(name_list_2[j]) + '\n')
            open('gg.csv', 'w+').write('\n'.join(op))
    await browser.close()
asyncio.get_event_loop().run_until_complete(main())

for n in range(len(name_list_2)):
    name_list_2[n] = ','.join(name_list_2[n])
name_list_2 = '\n'.join(name_list_2)

open('new.csv', 'w+').write(name_list_2)
