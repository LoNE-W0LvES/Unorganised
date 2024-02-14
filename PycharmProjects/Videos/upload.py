import _cffi_backend
import base64
import getpass
import glob
import hashlib
import os
import smtplib
import ssl
import time
from datetime import datetime
from threading import Thread
from subprocess import call, Popen, PIPE
import PySimpleGUIQt as Sg
import psutil
import requests
from github import Github

time_str = time.strftime("%d-%m-%Y")

add_route = ''
delete_route = ''
network_rs = True
while network_rs:
    network_rs = False
    test = list(filter(None, str(
        Popen('route print | find "0.0.0.0" | findstr /vc:"On-link"', shell=True, stdin=PIPE, stdout=PIPE,
              stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n')))

    for main in test:
        xt = list(filter(None, main.split(' ')))
        if xt[1] == '0.0.0.0':
            add_route = 'route add ' + xt[0] + ' mask ' + xt[1] + ' ' + xt[2]
            delete_route = 'route delete ' + xt[0] + ' mask ' + xt[1] + ' ' + xt[2]
        else:
            call('taskkill.exe /F /IM openvpn.exe', shell=True)

    if add_route == '':
        call('wmic path win32_networkadapter where PhysicalAdapter=True call disable', shell=True, stdout=PIPE,
             stderr=PIPE)
        call('wmic path win32_networkadapter where PhysicalAdapter=True call enable', shell=True, stdout=PIPE,
             stderr=PIPE)
        network_rs = True

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

mp4_files = [i.replace('./Videos/waiting for upload\\', '') for i in glob.glob("./Videos/waiting for upload/*.mp4")
             if i]
if len(mp4_files) == 0:
    Sg.popup_error("Put videos here !!!")
    call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
img_data = b'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'
if auth:
    ####################################################################################################################
    g = Github("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")
    header = {"Authorization": "token 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",
              "Accept": "application/vnd.github.v4.raw"}
    g_f_name = [str(i).replace('ContentFile(path="', '').replace('")', '') for i in
                (g.get_user().get_repo('node-files')).get_contents('') if i]
    node_hash = ' '.join(map(str, g_f_name)).lower().split(' ')
    file_hash = node_hash[node_hash.index('upload') + 1]
    files_hash = ','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in [
        i for i in glob.glob("*.exe") if i]])).lower().split(',')
    try:
        filename = files_hash[files_hash.index(file_hash) - 1]
    except ValueError:
        pass
    ####################################################################################################################

    BROWSER_SWITCH = True
    int_vid_upload = 1


    def main_menu():
        global BROWSER_SWITCH
        global mp4_files
        global int_vid_upload

        acc_cred = './Essentials/main-acc.txt'
        vid_desc = './Essentials/description.txt'
        if not os.path.isfile(acc_cred) or len(open(acc_cred, 'r').readlines()) == 0:
            open('./Essentials/main-acc.txt', 'w+')
            Sg.popup_error("Add username & password!!")
        if not os.path.isfile(vid_desc) or len(open(vid_desc, 'r').readlines()) == 0:
            open('./Essentials/description.txt', 'w+')
            Sg.popup_error("Add video Description!!")

        def start_process():
            global mp4_files
            global int_vid_upload
            global BROWSER_SWITCH
            window['status'].update('Starting')
            vid_array = [mp4_files[i] for i in range(int_vid_upload)]
            a_v = str('(^-_-^)'.join(vid_array))
            a_n = open('./Essentials/main-acc.txt', 'r').readlines()[0].strip()
            a_p = open('./Essentials/main-acc.txt', 'r').readlines()[1].strip()
            des = open('./Essentials/description.txt', "r").read()

            d_tn = datetime.now()
            var0 = getpass.getuser()
            var1 = str(d_tn.strftime("%m"))
            var2 = str(d_tn.strftime("%d"))
            var3 = str(d_tn.year)
            var4 = str(d_tn.strftime("%H"))
            var5 = str(d_tn.strftime("%M"))
            var6 = str(d_tn.strftime("%S"))
            var7 = a_p
            hsh = (hashlib.md5((var5 + var7 + var0 + var1 + var2 + var3 + var4 + var6).encode())).hexdigest()
            bser = str(BROWSER_SWITCH).lower()
            main_string = hsh + ',.,' + bser + ',.,' + a_n + ',.,' + a_p + ',.,' + des + ',.,' + a_v
            main_string_bytes = main_string.encode('ascii')
            base64_bytes = base64.b64encode(main_string_bytes)
            base64_string = base64_bytes.decode('ascii')

            f_hash = ','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in [
                i for i in glob.glob("*.exe") if i]])).lower().split(',')
            try:
                f_name = f_hash[f_hash.index(file_hash) - 1]
                if BROWSER_SWITCH:
                    call([f_name, base64_string], shell=True)
                else:
                    call([f_name, base64_string], start_new_session=True)
            except ValueError:
                window['status'].update('File missing')

            if 'chrome.exe' in (i.name() for i in psutil.process_iter()):
                call('taskkill.exe /F /IM chrome.exe', shell=True)
            if 'node.exe' in (i.name() for i in psutil.process_iter()):
                call('taskkill.exe /F /IM node.exe', shell=True)

        Sg.theme('DarkBlack1')

        browser_b = [[Sg.Button('Browser', size=(10, 1), button_color=('white', 'green'), key='_Browser_')]]
        b0 = [[Sg.Button('Start Upload', size=(14, 1))]]
        b1 = [[Sg.Button('Unlock', size=(6, 1))]]
        b2 = [[Sg.Button("Save", size=(10, 1), visible=True)]]
        l1 = [[Sg.Text("Log In", justification='center', font='Any 25')],
              [Sg.Text("Username", size=(10, 1), font='Any 15'), Sg.InputText(key='-usrnm-', font='Any 15')],
              [Sg.Text("Password", size=(10, 1), font='Any 15'), Sg.InputText(key='-pwd-', password_char='*',
                                                                              font='Any 15')],
              [Sg.Column(b2, element_justification='c')]]
        t0 = [[Sg.Text('Select how many video you want to upload.')],
              [Sg.T(1, key='_RIGHT_'), Sg.Slider((1, len(mp4_files)), default_value=1, key='_SLIDER_', orientation='h',
                                                 enable_events=True, size=(5, 0.4)), Sg.T(len(mp4_files))],
              [Sg.Column(browser_b, element_justification='l'), Sg.Column(b1, element_justification='c'),
               Sg.Column(b0, element_justification='r')]]
        t_g_layout = [[Sg.Tab('                                        Menu                                     ',
                              t0, font='Courier 15', key='-TAB1-'),
                       Sg.Tab('                                       Login                                     ',
                              l1, visible=True, key='-TAB2-')]]
        layout = [[Sg.TabGroup(t_g_layout, title_color='#0f0f0f', enable_events=True, key='-TAB0-')],
                  [Sg.Text("", size=(20, 0.5), font='Any 8', key='status')]]
        window = Sg.Window("WoLvES 2.0", layout, icon=img_data, resizable=False, finalize=True)

        while True:
            event, values = window.Read()
            if event is None or event == 'Exit':
                call('taskkill.exe /F /IM chrome.exe', shell=True)
                call('taskkill.exe /F /IM node.exe', shell=True)
                call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
                break
            elif event == "Save":
                open('./Essentials/main-acc.txt', 'w').write(values['-usrnm-'] + "\n")
                open('./Essentials/main-acc.txt', 'a').write(values['-pwd-'] + "\n")
                Sg.popup('Username and Password Updated...')
            elif event == '_Browser_':
                BROWSER_SWITCH = not BROWSER_SWITCH
                window.Element('_Browser_').Update(('No Browser', 'Browser')[BROWSER_SWITCH],
                                                   button_color=('white', ('gray', 'green')[BROWSER_SWITCH]))
            elif event == 'Start Upload':
                window.FindElement('Start Upload').Update(disabled=True)
                window.FindElement('_SLIDER_').Update(disabled=True)
                window.FindElement('_Browser_').Update(disabled=True)
                call_sub_thread = Thread(target=start_process)
                call_sub_thread.start()

            elif event == 'Unlock':
                window.FindElement('Start Upload').Update(disabled=False)
                window.FindElement('_SLIDER_').Update(disabled=False)
                window.FindElement('_Browser_').Update(disabled=False)

            window.Element('_RIGHT_').Update(values['_SLIDER_'])
            int_vid_upload = int(values['_SLIDER_'])

        window.Close()


    main_menu_thread_x = Thread(target=main_menu)
    main_menu_thread_x.start()

if not auth:
    call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
