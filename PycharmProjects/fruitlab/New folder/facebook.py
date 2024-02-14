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
from github import Github


if not os.path.isfile('./Group.txt') or len(open('./Group.txt', 'r').readlines()) == 0:
    open('./Group.txt', 'w+')
    Sg.popup_error("Add Groups!!")
if not os.path.isfile('./auth.txt'):
    open('./auth.txt', 'w+')

o_message = ''
if os.path.isfile('./fb-message.txt'):
    o_message = "".join(line for line in open('./fb-message.txt') if not line.isspace())
    open('./fb-message.txt', 'w+').write(o_message)

clean = "".join(line for line in open('./Group.txt') if not line.isspace())
open('./Group.txt', 'w+').write(clean)
g_array = [i.replace('\n', '') for i in open('./Group.txt').readlines()]
description = ''
BROWSER_SWITCH = True


def start_work():
    global BROWSER_SWITCH
    global description
    window['status'].update('Starting')
    group_arr = [i.replace('\n', '') for i in open('./Group.txt').readlines()]
    grp = '(^_^)'.join(group_arr)
    fb_user = open('./auth.txt', 'r').readlines()[0].strip()
    fb_pass = open('./auth.txt', 'r').readlines()[1].strip()

    hsh = ''
    bser = str(BROWSER_SWITCH).lower()
    main_string = hsh + ',.,' + bser + ',.,' + fb_user + ',.,' + fb_pass + ',.,' + description + ',.,' + grp
    main_string_bytes = main_string.encode('ascii')
    base64_bytes = base64.b64encode(main_string_bytes)
    base64_string = base64_bytes.decode('ascii')

    f_hash = ','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in [
        i for i in glob.glob("*.exe") if i]])).lower().split(',')
    try:
        f_name = 'facebook-node.exe'
        if BROWSER_SWITCH:
            call([f_name, base64_string], shell=True)
            window['status'].update('Done')
        else:
            call([f_name, base64_string], start_new_session=True)
            window['status'].update('Done')
    except ValueError:
        window['status'].update('File missing')

    if 'node.exe' in (i.name() for i in psutil.process_iter()):
        call('taskkill.exe /F /IM node.exe', shell=True)


message = [[Sg.Multiline(o_message, size=(67, 19), key='message')]]

browser_b = [[Sg.Button('Browser', size=(10, 1), button_color=('white', 'green'), key='_Browser_'),
              Sg.Button('Start', size=(14, 1))]]
group = [[Sg.Listbox(values=g_array, enable_events=True, size=(67, 14), select_mode=Sg.LISTBOX_SELECT_MODE_SINGLE,
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
        call_sub_thread = Thread(target=start_work)
        call_sub_thread.start()

    elif event == 'Unlock':
        window['Start'].Update(disabled=False)
        window['_Browser_'].Update(disabled=False)