import base64
import getpass
import glob
import hashlib
import os
import smtplib
import ssl
from subprocess import call, Popen, PIPE
from threading import Thread
import PySimpleGUI as Sg
import psutil
import asyncio
from pyppeteer import launch

fb = open('./auth.txt', 'r').readlines()
fb_user = fb[0].strip().replace('\n', '')
fb_pass = fb[1].strip().replace('\n', '')
fb.clear()
description = ''
BROWSER_SWITCH = True


async def main():
    global description
    global BROWSER_SWITCH
    chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    browser = await launch(args=['--window-size=1700,900'], headless=False, executablePath=chrome)
    page = await browser.newPage()
    await page.setViewport({'width': 1700, 'height': 900})

    await page.goto('https://www.facebook.com', {'waituntil': 'networkidle2', 'timeout': 0})

    await page.waitFor(1000)

    await page.waitForSelector('button[name="login"]')
    await page.type('input[name="email"]', fb_user, {'delay': 60})
    await page.type('input[name="pass"]', fb_pass, {'delay': 50})

    try:
        await page.click('button[name="login"]')
    except Exception as e:
        print(e)

    try:
        await page.click('button[type="submit"]')
    except Exception as e:
        print(e)
    await page.waitFor(5000)
    await page.waitFor("[name=__CONFIRM__]")
    await page.keyboard.press("Escape")

    await page.waitFor(5000)
    page_urls = [i.replace('\n', '') for i in open('./Group.txt').readlines()]
    for url in page_urls:

        await page.goto(url, {'waituntil':'networkidle2', 'timeout': 0})
        await page.waitForSelector('div[class="m9osqain a5q79mjw gy2v8mqq jm1wdb64 k4urcfbm qv66sw1b"]');
        await page.click('div[class="m9osqain a5q79mjw gy2v8mqq jm1wdb64 k4urcfbm qv66sw1b"]');
        await page.waitFor(5000)
        await page.click('div[class="gcieejh5 bn081pho humdl8nn izx4hr6d rq0escxv oo9gr5id t5a262vz o0t2es00 b1v8xokw datstx6m f530mmz5 lzcic4wl ecm0bbzt rz4wbd8a sj5x9vvc a8nywdso k4urcfbm o8yuz56k"]')
        await page.waitFor(5000)
        await page.type('div[class="gcieejh5 bn081pho humdl8nn izx4hr6d rq0escxv oo9gr5id t5a262vz o0t2es00 b1v8xokw datstx6m f530mmz5 lzcic4wl ecm0bbzt rz4wbd8a sj5x9vvc a8nywdso k4urcfbm o8yuz56k"]', description, {'delay': 50})
        await page.waitFor(25000)
        await page.click('div[aria-label="Post"]')
        await page.waitFor(25000)

    await page.waitFor(5000)
    # await browser.close()


# if not os.path.isfile('./Group.txt') or len(open('./Group.txt', 'r').readlines()) == 0:
#     open('./Group.txt', 'w+')
#     Sg.popup_error("Add Groups!!")
# if not os.path.isfile('./auth.txt'):
#     open('./auth.txt', 'w+')

# o_message = ''
# # if os.path.isfile('./fb-message.txt'):
# #     o_message = "".join(line for line in open('./fb-message.txt') if not line.isspace())
# #     open('./fb-message.txt', 'w+').write(o_message)
#
# clean = "".join(line for line in open('./Group.txt') if not line.isspace())
# open('./Group.txt', 'w+').write(clean)
# g_array = [i.replace('\n', '') for i in open('./Group.txt').readlines()]


def start_work():
    global BROWSER_SWITCH
    global description
    # window['status'].update('Starting')
    asyncio.run(main())


message = [[Sg.Multiline('o_message', size=(67, 19), key='message')]]

browser_b = [[Sg.Button('Browser', size=(10, 1), button_color=('white', 'green'), key='_Browser_'),
              Sg.Button('Start', size=(14, 1))]]
group = [[Sg.Listbox(values=['g_array'], enable_events=True, size=(67, 14), select_mode=Sg.LISTBOX_SELECT_MODE_SINGLE,
                     key='-GROUP-LIST-')], [Sg.Button('Delete', disabled=True, size=(60, 1))],
         [Sg.InputText(key='-GROUP-', size=(60, 1), font='Any 10'), Sg.Button('ADD', size=(6, 1))]]

b2 = [[Sg.Button("Save", size=(10, 1), visible=True)]]
l1 = [[Sg.Text("Log In", justification='center', font='Any 25')],
      [Sg.Text("Username", size=(10, 1), font='Any 15')],
      [Sg.InputText(key='-usrnm-', size=(67, 2), font='Any 10')],
      [Sg.Text("Password", size=(10, 1), font='Any 15')],
      [Sg.InputText(key='-pwd-', size=(67, 2), password_char='*', font='Any 10')],
      [Sg.Column(b2, element_justification='c')]]

t_g_layout = [[Sg.Tab('Group', group, key='-GROUP-T-'),
               Sg.Tab('Message', message, key='-Message-'),
               Sg.Tab('LogIn', l1, key='-LogIn-')]]

layout = [[Sg.Column(browser_b, element_justification='r')],
          [Sg.TabGroup(t_g_layout, title_color='#0f0f0f', enable_events=True, key='-TAB0-')],
          [Sg.Column([[Sg.Button('Unlock', size=(6, 1))]], element_justification='r')],
          [Sg.Text("", size=(20, 1), font='Any 8', key='status')]]

window = Sg.Window("WoLvES 2.0", layout, resizable=False, finalize=True)

# print(type window)
# def check_auth():
#     switch = True
#     while True:
#         if not os.path.isfile('./auth.txt') or len(open('./auth.txt', 'r').readlines()) == 0:
#             if switch:
#                 switch = False
#                 window['Start'].Update(disabled=True)
#                 window['-GROUP-T-'].Update(disabled=True)
#                 window['-Message-'].Update(disabled=True)
#                 window['Unlock'].Update(disabled=True)
#         else:
#             if not switch:
#                 switch = True
#                 window['Start'].Update(disabled=False)
#                 window['-GROUP-T-'].Update(disabled=False)
#                 window['-Message-'].Update(disabled=False)
#                 window['Unlock'].Update(disabled=False)
#
#
# check_auth_thread = Thread(target=check_auth)
# check_auth_thread.start()

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        call('taskkill.exe /F /IM node.exe', shell=True)
        call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
        break

    elif event == '_Browser_':
        BROWSER_SWITCH = not BROWSER_SWITCH
        window.Element('_Browser_').Update(('No Browser', 'Browser')[BROWSER_SWITCH],
                                           button_color=('white', ('gray', 'green')[BROWSER_SWITCH]))
    elif event == "ADD":
        g_input = values['-GROUP-']
        if g_input != '':
            if 'facebook.com' in g_input or 'fb.com' in g_input:
                try:
                    g_n_c_array = [i.replace('\n', '') for i in open('./Group.txt').readlines()]
                    if g_input not in g_n_c_array:
                        open('./Group.txt', 'a').write(g_input + "\n")
                    clean = "".join(line for line in open('./Group.txt') if not line.isspace())
                    open('./Group.txt', 'w+').write(clean)
                    g_c_array = [i.replace('\n', '') for i in open('./Group.txt').readlines()]
                    window['-GROUP-LIST-'].Update(g_c_array)
                    window['-GROUP-'].Update('')
                except FileNotFoundError:
                    open('./Group.txt', 'w+')

    if event == '-GROUP-LIST-':
        window['Delete'].Update(disabled=False)

    elif event == "Delete":
        group_array = open('./Group.txt').readlines()
        group_array.remove(values['-GROUP-LIST-'][0].strip() + '\n')
        clean = "".join(line for line in group_array if not line.isspace())
        n_g_array = ''.join(clean)
        open('./Group.txt', 'w').write(n_g_array)

        n_array = [k.replace("\n", "") for k in group_array]
        window['-GROUP-LIST-'].Update(n_array)

    elif event == "Save":
        if values['-usrnm-'] != '' or values['-pwd-'] != '' or values['-pwd-'] != ' ' or values['-usrnm-'] != ' ':
            print('t')
            open('./auth.txt', 'w').write(values['-usrnm-'] + "\n")
            open('./auth.txt', 'a').write(values['-pwd-'] + "\n")
            window['-usrnm-'].Update('')
            window['-pwd-'].Update('')
            Sg.popup('Username and Password Updated...')

    elif event == 'Start':
        description = '\n'.join([i for i in values['message'].split('\n') if i])
        open('./fb-message.txt', 'w+').write(description)
        o_mess = "".join(line for line in open('./fb-message.txt') if not line.isspace())
        open('./fb-message.txt', 'w+').write(o_mess)
        window['Start'].Update(disabled=True)
        window['_Browser_'].Update(disabled=True)
        # start_thread = Thread(target=start_work)
        # start_thread.start()
        asyncio.run(main())

    elif event == 'Unlock':
        window['Start'].Update(disabled=False)
        window['_Browser_'].Update(disabled=False)












# import asyncio
# from pyppeteer import launch
#
# fb = open('./auth.txt', 'r').readlines()
# fb_user = fb[0].strip().replace('\n', '')
# fb_pass = fb[1].strip().replace('\n', '')
# fb.clear()
# description = ''
# BROWSER_SWITCH = True
#
#
# async def main():
#     global description
#     global BROWSER_SWITCH
#     chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
#     browser = await launch(args=['--window-size=1700,900'], headless=False, executablePath=chrome)
#     page = await browser.newPage()
#     await page.setViewport({'width': 1700, 'height': 900})
#
#     await page.goto('https://www.facebook.com', {'waituntil': 'networkidle2', 'timeout': 0})
#
#     await page.waitFor(1000)
#
#     await page.waitForSelector('button[name="login"]')
#     await page.type('input[name="email"]', fb_user, {'delay': 60})
#     await page.type('input[name="pass"]', fb_pass, {'delay': 50})
#
#     try:
#         await page.click('button[name="login"]')
#     except Exception as e:
#         print(e)
#
#     try:
#         await page.click('button[type="submit"]')
#     except Exception as e:
#         print(e)
#     await page.waitFor(5000)
#     await page.waitFor("[name=__CONFIRM__]")
#     await page.keyboard.press("Escape")
#
#
#     await page.waitFor(5000)
#     page_urls = [i.replace('\n', '') for i in open('./Group.txt').readlines()]
#     for url in page_urls:
#
#         await page.goto(url, {'waituntil':'networkidle2', 'timeout': 0})
#         await page.waitForSelector('div[class="m9osqain a5q79mjw gy2v8mqq jm1wdb64 k4urcfbm qv66sw1b"]');
#         await page.click('div[class="m9osqain a5q79mjw gy2v8mqq jm1wdb64 k4urcfbm qv66sw1b"]');
#         await page.waitFor(5000)
#         await page.click('div[class="gcieejh5 bn081pho humdl8nn izx4hr6d rq0escxv oo9gr5id t5a262vz o0t2es00 b1v8xokw datstx6m f530mmz5 lzcic4wl ecm0bbzt rz4wbd8a sj5x9vvc a8nywdso k4urcfbm o8yuz56k"]')
#         await page.waitFor(5000)
#         await page.type('div[class="gcieejh5 bn081pho humdl8nn izx4hr6d rq0escxv oo9gr5id t5a262vz o0t2es00 b1v8xokw datstx6m f530mmz5 lzcic4wl ecm0bbzt rz4wbd8a sj5x9vvc a8nywdso k4urcfbm o8yuz56k"]', description, {'delay': 50})
#         await page.waitFor(25000)
#         await page.click('div[aria-label="Post"]')
#         await page.waitFor(25000)
#
#     await page.waitFor(5000)
#     # await browser.close()
#
#
# asyncio.run(main())
# def wait_for_page_load(self, timeout=10):
#     self.log.debug("Waiting for page to load at {}.".format(self.driver.current_url))
#     old_page = self.find_element_by_tag_name('html')
#     yield
#     WebDriverWait(self, timeout).until(ec.staleness_of(old_page))
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys

fb = open('./auth.txt', 'r').readlines()
fb_user = fb[0].strip().replace('\n', '')
fb_pass = fb[1].strip().replace('\n', '')
fb.clear()
description = 'hii'
BROWSER_SWITCH = True


def slow_type(element: WebElement, text: str):
    for character in text:
        element.send_keys(character)
        time.sleep(0.05)


def page_is_loading(drive):
    while True:
        x = drive.execute_script("return document.readyState")
        if x == "complete":
            return True
        else:
            yield False


def post_on_facebook(self, group_url):

    print('Posting  on Facebook group: ', group_url)

    time.sleep(4)
    self.browser.get(group_url)
    time.sleep(2)

    text_to_post = 'The content to post goes here'

    try:
        post_class = 'oajrlxb2 b3i9ofy5 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 j83agx80 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x cxgpxx05 d1544ag0 sj5x9vvc tw6a2znq i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l bp9cbjyn orhb3f3m czkt41v7 fmqxjp7s emzo65vh btwxx1t3 buofh1pr idiwt2bm jifvfom9 kbf60n1y'
        post_class = post_class.replace(' ', '.')
        click_post = self.browser.find_element_by_class_name(post_class)
        click_post.click()
        time.sleep(5)

        post_content = self.browser.find_element_by_class_name('notranslate._5rpu')
        post_content = self.browser.switch_to_active_element()
        post_content.send_keys(text_to_post)
        time.sleep(5)

        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        all_pc = soup.find_all('div', attrs={'id': re.compile("^mount_0_0_")})
        id_ = str(all_pc[0].get('id'))
        xpath = '//*[@id="' + id_ + '"]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div[1]/div'
        post = self.browser.find_element_by_xpath(xpath)
        post.click()
        time.sleep(5)

    except:
        print("Something went wrong, exiting script to avoid conflicts")



options = webdriver.ChromeOptions()
pref = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs", pref)
driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome('./chromedriver')

driver.get('https://www.facebook.com')
while not page_is_loading(driver):
    continue

input_user = WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.NAME, "email")))
slow_type(input_user, fb_user)

input_pass = WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.NAME, "pass")))
slow_type(input_pass, fb_pass)

input_pass.send_keys(Keys.ENTER)
time.sleep(5)
page_urls = [i.replace('\n', '') for i in open('./Group.txt').readlines()]
for url in page_urls:
    while not page_is_loading(driver):
        continue
    driver.get(url)

    #         await page.waitForSelector('div[class="m9osqain a5q79mjw gy2v8mqq jm1wdb64 k4urcfbm qv66sw1b"]');
    #         await page.click('div[class="m9osqain a5q79mjw gy2v8mqq jm1wdb64 k4urcfbm qv66sw1b"]');

    inputTClick = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="m9osqain a5q79mjw gy2v8mqq jm1wdb64 k4urcfbm qv66sw1b"]'))).click()
    # time.sleep(5)
    # await page.click('div[class="gcieejh5 bn081pho humdl8nn izx4hr6d rq0escxv oo9gr5id t5a262vz o0t2es00 b1v8xokw datstx6m f530mmz5 lzcic4wl ecm0bbzt rz4wbd8a sj5x9vvc a8nywdso k4urcfbm o8yuz56k"]')
    #         await page.waitFor(5000)
    #         await page.type('div[class="gcieejh5 bn081pho humdl8nn izx4hr6d rq0escxv oo9gr5id t5a262vz o0t2es00 b1v8xokw datstx6m f530mmz5 lzcic4wl ecm0bbzt rz4wbd8a sj5x9vvc a8nywdso k4urcfbm o8yuz56k"]', description, {'delay': 50})
    #         await page.waitFor(25000)
    inputTWrite = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'div[class="gcieejh5 bn081pho humdl8nn izx4hr6d rq0escxv oo9gr5id t5a262vz o0t2es00 b1v8xokw datstx6m f530mmz5 lzcic4wl ecm0bbzt rz4wbd8a sj5x9vvc a8nywdso k4urcfbm o8yuz56k"]')))
    inputTWrite.click()
    slow_type(inputTWrite, description)
    inputTWrite.send_keys(description)

    time.sleep(5)
    # message = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div')
    # slow_type(message, description)
    # message.send_keys(description)

    # slow_type(fb_posting[1], description)





#mount_0_0_LL > div > div:nth-child(1) > div > div:nth-child(7) > div > div > div.rq0escxv.l9j0dhe7.du4w35lb > div > div.iqfcb0g7.tojvnm2t.a6sixzi8.k5wvi7nf.q3lfd5jv.pk4s997a.bipmatt0.cebpdrjk.qowsmv63.owwhemhu.dp1hu0rb.dhp61c6y.l9j0dhe7.iyyx5f41.a8s20v7p > div > div > div > div > div.rq0escxv.pmk7jnqg.du4w35lb.pedkr2u6.oqq733wu.ms05siws.pnx7fd3z.b7h9ocf4.j9ispegn.kr520xx4 > form > div > div.rq0escxv.pmk7jnqg.du4w35lb.pedkr2u6.oqq733wu.ms05siws.pnx7fd3z.b7h9ocf4.j9ispegn.kr520xx4 > div > div > div.j83agx80.btwxx1t3.s8dhs3de.mfofr4af.hihg3u9x.ggxiycxj.hjequu9d.ssoat4ej.f344zkr0.s9tcezmb > div > div.q5bimw55.rpm2j7zs.k7i0oixp.gvuykj2m.j83agx80.cbu4d94t.ni8dbmo4.eg9m0zos.l9j0dhe7.du4w35lb.ofs802cu.pohlnb88.dkue75c7.mb9wzai9.l56l04vs.r57mb794.kh7kg01d.c3g1iek1.buofh1pr > div.j83agx80.cbu4d94t.buofh1pr.l9j0dhe7 > div.o6r2urh6.buofh1pr.datstx6m.l9j0dhe7.k4urcfbm > div.rq0escxv.buofh1pr.df2bnetk.hv4rvrfc.dati1w0a.l9j0dhe7.k4urcfbm.du4w35lb.gbhij3x4 > div > div
# search_bar = driver.find_element_by_name("q")
# search_bar.clear()
# search_bar.send_keys("getting started with python")
# search_bar.send_keys(Keys.RETURN)
# print(driver.current_url)
# driver.close()



