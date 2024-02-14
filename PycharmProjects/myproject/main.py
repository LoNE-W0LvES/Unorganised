import re

import glob
import os


from refextract import extract_references_from_file

from Essentials import essential

from subprocess import call
import PySimpleGUI as Sg
import asyncio
from pyppeteer import launch

from os.path import isfile

if not isfile('./bib.txt'):
    open('bib.txt', 'w+')

if not isfile('./ref-data.txt'):
    open('ref-data.txt', 'w+')


def get_bib(refer):
    async def main_x():
        browser = await launch(args=['--window-size=1920,1080'], defaultViewport=None, headless=False)
        page = await browser.newPage()
        print(refer)
        for ff in range(len(refer)):
            print(refer[ff])
            await page.goto('https://scholar.google.com/')
            await page.type('#gs_hdr_tsi', refer[ff])
            await page.keyboard.press('Enter')
            # if ff == 0:
            #     sleep(50)
            await page.waitFor(500)
            await page.waitForSelector(
                '#gs_res_ccl_mid > div > div.gs_ri > div.gs_fl.gs_flb > a.gs_or_cit.gs_or_btn.gs_nph > span')
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
            print(text)

    asyncio.run(main_x())


def main():
    pdf_layout = []
    pdf_to_read = []
    essential()
    pdf_names = [i.replace('./pdf\\', '') for i in glob.glob("./pdf/*.pdf") if i]

    for i in range(len(pdf_names)):
        pdf_layout += [[Sg.Text('', size=(1, 1))], [Sg.Checkbox(pdf_names[i], enable_events=True, disabled=False, key=f'-check{i}-')]]

    layout = [[Sg.Column(pdf_layout, size=(590, 590), scrollable=True)], [Sg.Button('Continue', disabled=False, size=(60, 1))]]
    #
    window = Sg.Window("WoLvES 2.0", layout, resizable=False, finalize=True)
    while True:
        event, values = window.read()
        if event == Sg.WINDOW_CLOSED:
            window.close()
            # call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
            break
        elif event == 'Continue':
            for i in range(len(pdf_names)):
                window[f'-check{i}-'].update(disabled=True)
            window['Continue'].update(disabled=True)
            window.hide()
            ref_data = []
            for pdf in pdf_names:
                references = []
                ref = extract_references_from_file(pdf)
                for i in ref:
                    if i['raw_ref'][0] not in references:
                        references.append(i['raw_ref'][0])

                f_ref, nf_ref, temp = [], [], []

                for line in references:
                    if line.endswith("."):
                        if bool(re.findall(r'\[\d+\]', line)):
                            for t in temp:
                                f_ref.append(t.strip())
                            temp.clear()
                        f_ref.append((" ".join(temp) + " " + line).strip() if temp else line.strip())
                        temp.clear()
                    else:
                        temp.append(line)

                for line in f_ref:
                    if [x for x in [re.findall(pattern, line) for pattern in
                                    [r'\(\d{4}, [A-Za-z]+\)', r'\([A-Za-z]+, \d{4}\)', r'\((\d{4})\)']] if x]:
                        if bool(re.findall(r'\[\d+\]', line)):
                            nf_ref.append(line)
                            temp.clear()
                        else:
                            nf_ref.append((" ".join(temp)).strip() if len(temp) == 0 else "".join(temp).strip())
                        temp.clear()
                        temp.append(line)
                    else:
                        if bool(re.findall(r'\[\d+\]', line)):
                            nf_ref.append(line)
                            temp.clear()
                        temp.append(line)

                nf_ref = [re.sub(r'\[\d+\]', '', x) for x in nf_ref if x]
                ref_data.extend(nf_ref)
            open('ref-data.txt', 'w', encoding="utf-8").write('\n'.join(ref_data))
            ref_layout = []
            ref_to_cite = []
            for i in range(len(ref_data)):
                ref_layout += [[Sg.Text('', size=(1, 1))],
                               [Sg.Checkbox(ref_data[i], enable_events=True, disabled=False, key=f'-r-check{i}-')]]

            layout = [[Sg.Column(ref_layout, size=(590, 590), scrollable=True)],
                      [Sg.Button('Continue', disabled=False, size=(60, 1))]]
            window = Sg.Window("Cite", layout, resizable=False, finalize=True)

            while True:
                event, values = window.read()
                if event == Sg.WINDOW_CLOSED:
                    window.close()
                    call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
                    break
                elif event == 'Continue':
                    for i in range(len(ref_data)):
                        window[f'-r-check{i}-'].update(disabled=True)
                    window['Continue'].update(disabled=True)
                    window.hide()
                    get_bib(ref_to_cite)

                for i in range(len(ref_data)):
                    if event == f'-r-check{i}-':
                        if values[f'-r-check{i}-']:
                            ref_to_cite.append(ref_data[i])
                        else:
                            ref_to_cite.remove(ref_data[i])

            window.close()
        for i in range(len(pdf_names)):
            if event == f'-check{i}-':
                if values[f'-check{i}-']:
                    pdf_to_read.append(pdf_names[i])
                else:
                    pdf_to_read.remove(pdf_names[i])


main()
