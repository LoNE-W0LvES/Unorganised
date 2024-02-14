import getpass
import os
import smtplib
import ssl
import time
from subprocess import call, Popen, PIPE
from threading import Thread

import PySimpleGUI as Sg
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

auth = False
hw_id = str(Popen('wmic csproduct get uuid', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()[0]
            ).split('\\r\\n')[1].strip('\\r').strip()
try:
    data = requests.get('https://pastebin.com/raw/y9e52zB6').text
    if hw_id in data:
        auth = True
    else:
        Sg.popup("Failed to Authenticate")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as server:
            server.login('w3961500@gmail.com', 'wolvesbatch00')
            server.sendmail('w3961500@gmail.com', 'wolvesbatch1@gmail.com', getpass.getuser() + '\n' + hw_id)
        Sg.popup("Wait for Verification")
        call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
except requests.exceptions.ConnectionError:
    Sg.popup("DNS/Server issue or No Internet Connection")
    call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)

if auth:
    description = ''
    BROWSER_SWITCH = True
    fb = open('./auth.txt', 'r').readlines()
    fb_user = fb[0].strip().replace('\n', '')
    fb_pass = fb[1].strip().replace('\n', '')
    fb.clear()

    if not os.path.isfile('./Group.txt') or len(open('./Group.txt', 'r').readlines()) == 0:
        open('./Group.txt', 'w+')
        Sg.popup_error("Add Groups!!")
    if not os.path.isfile('./auth.txt'):
        open('./auth.txt', 'w+')
    if os.path.isfile('./fb-message.txt'):
        description = ''.join(line for line in open('./fb-message.txt') if line)
        open('./fb-message.txt', 'w+').write(description)
    group_clean = "".join(line for line in open('./Group.txt') if not line.isspace())
    open('./Group.txt', 'w+').write(group_clean)

    page_urls = [i.replace('\n', '') for i in open('./Group.txt').readlines()]

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


    def fb_browser():
        global fb_user
        global fb_pass
        global page_urls
        global description
        global BROWSER_SWITCH
        options = webdriver.ChromeOptions()
        pref = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", pref)
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.facebook.com')
        while not page_is_loading(driver):
            continue
        input_user = WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.NAME, "email")))
        slow_type(input_user, fb_user)
        input_pass = WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.NAME, "pass")))
        slow_type(input_pass, fb_pass)
        input_pass.send_keys(Keys.ENTER)
        time.sleep(5)

        for url in page_urls:
            while not page_is_loading(driver):
                continue
            driver.get(url)
            try:
                time.sleep(5)
                WebDriverWait(driver, 10).until(ec.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'div[class="m9osqain a5q79mjw gy2v8mqq jm1wdb64 k4urcfbm qv66sw1b"]'))).click()
                time.sleep(5)
                post_content = driver.find_element_by_class_name('notranslate._5rpu')
                slow_type(post_content, description)
                time.sleep(5)
                WebDriverWait(driver, 10).until(
                    ec.visibility_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Post"]'))).click()
            except AttributeError:
                window['status'].update('Element not found')
        window['status'].update('Done')


    message = [[Sg.Multiline(description, size=(67, 19), key='message')]]

    browser_b = [[Sg.Button('Browser', size=(10, 1), button_color=('white', 'green'), key='_Browser_'),
                  Sg.Button('Start', size=(14, 1))]]
    grp = [[Sg.Listbox(values=page_urls, enable_events=True, size=(67, 14), select_mode=Sg.LISTBOX_SELECT_MODE_SINGLE,
                       key='-GROUP-LIST-')], [Sg.Button('Delete', disabled=True, size=(60, 1))],
           [Sg.InputText(key='-GROUP-', size=(60, 1), font='Any 10'), Sg.Button('ADD', size=(6, 1))]]

    b2 = [[Sg.Button("Save", size=(10, 1), visible=True)]]
    l1 = [[Sg.Text("Log In", justification='center', font='Any 25')],
          [Sg.Text("Username", size=(10, 1), font='Any 15')],
          [Sg.InputText(fb_user, key='-usr-', size=(67, 2), font='Any 10')],
          [Sg.Text("Password", size=(10, 1), font='Any 15')],
          [Sg.InputText(fb_pass, key='-pwd-', size=(67, 2), password_char='*', font='Any 10')],
          [Sg.Column(b2, element_justification='c')]]

    t_g_layout = [[Sg.Tab('Group', grp, key='-GROUP-T-'),
                   Sg.Tab('Message', message, key='-Message-'),
                   Sg.Tab('LogIn', l1, key='-LogIn-')]]

    layout = [[Sg.Column(browser_b, element_justification='r')],
              [Sg.TabGroup(t_g_layout, title_color='#0f0f0f', enable_events=True, key='-TAB0-')],
              [Sg.Column([[Sg.Button('Unlock', size=(6, 1))]], element_justification='r')],
              [Sg.Text("", size=(20, 1), font='Any 8', key='status')]]

    window = Sg.Window("WoLvES 2.0", layout, resizable=False, finalize=True)


    def check_auth():
        switch = True
        while True:
            if not os.path.isfile('./auth.txt') or len(open('./auth.txt', 'r').readlines()) == 0:
                if switch:
                    switch = False
                    window['Start'].Update(disabled=True)
                    window['-GROUP-T-'].Update(disabled=True)
                    window['-Message-'].Update(disabled=True)
                    window['Unlock'].Update(disabled=True)
            else:
                if not switch:
                    switch = True
                    window['Start'].Update(disabled=False)
                    window['-GROUP-T-'].Update(disabled=False)
                    window['-Message-'].Update(disabled=False)
                    window['Unlock'].Update(disabled=False)


    check_auth_thread = Thread(target=check_auth)
    check_auth_thread.start()

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
            page_urls.remove(values['-GROUP-LIST-'][0].strip())
            window['-GROUP-LIST-'].Update(page_urls)
            n_array = '\n'.join(line for line in page_urls if not line.isspace())
            open('./Group.txt', 'w').write(n_array)

        elif event == "Save":
            if values['-usr-'] != '' or values['-pwd-'] != '' or values['-pwd-'] != ' ' or values['-usr-'] != ' ':
                fb_user = values['-usr-']
                fb_pass = values['-pwd-']
                open('./auth.txt', 'w').write(fb_user + "\n")
                open('./auth.txt', 'a').write(fb_pass + "\n")
                window['-usr-'].Update(fb_user)
                window['-pwd-'].Update(fb_pass)
                Sg.popup('Username and Password Updated...')

        elif event == 'Start':
            description = values['message']
            print(description)
            open('./fb-message.txt', 'w+').write(description)
            window['status'].update('Starting')
            window['Start'].Update(disabled=True)
            window['_Browser_'].Update(disabled=True)
            start_thread = Thread(target=fb_browser)
            start_thread.start()

        elif event == 'Unlock':
            window['Start'].Update(disabled=False)
            window['_Browser_'].Update(disabled=False)

if not auth:
    call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
