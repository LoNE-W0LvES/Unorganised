import _cffi_backend
import base64
import getpass
import glob
import hashlib
import os
import random
import smtplib
import ssl
import string
from subprocess import call, Popen, PIPE
import time
from datetime import datetime
from io import StringIO
from threading import Thread
from urllib import parse

import PySimpleGUIQt as Sg
import pandas as pd
import psutil
import requests
from github import Github

time_str = time.strftime("%d-%m-%Y")
auth = False

acc_f_path = './Essentials/AccCount-c.txt'
vi_f_path = './Essentials/UsedIPs.txt'
open(vi_f_path, 'w+')
add_route = ''
delete_route = ''


def restart_net():
    global add_route
    global delete_route
    network_rs = True
    while network_rs:
        network_rs = False
        net_look = list(filter(None, str(
            Popen('route print | find "0.0.0.0" | findstr /vc:"On-link"', shell=True, stdin=PIPE, stdout=PIPE,
                  stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n')))

        for main in net_look:
            xt = list(filter(None, main.split(' ')))
            if xt[1] == '0.0.0.0':
                add_route = 'route add ' + xt[0] + ' mask ' + xt[1] + ' ' + xt[2]
                delete_route = 'route delete ' + xt[0] + ' mask ' + xt[1] + ' ' + xt[2]

        if add_route == '':
            call('wmic path win32_networkadapter where PhysicalAdapter=True call disable',
                 shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            call('wmic path win32_networkadapter where PhysicalAdapter=True call enable',
                 shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            network_rs = True


restart_net()

g = Github("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")
header = {"Authorization": "token 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", "Accept": "application/vnd.github.v4.raw"}
g_f_name = [str(i).replace('ContentFile(path="', '').replace('")', '') for i in
            (g.get_user().get_repo('node-files')).get_contents('') if i]
node_hash = ' '.join(map(str, g_f_name)).split(' ')
file_hash = node_hash[node_hash.index('create') + 1]


def cleanup():
    if 'openvpn.exe' in (i.name() for i in psutil.process_iter()):
        call('taskkill.exe /F /IM openvpn.exe', shell=True)

    f_has = ','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in [
        i for i in glob.glob("*.exe") if i]])).split(',')
    try:
        f_nam = f_has[f_has.index(file_hash) - 1]
        if f_nam in (i.name() for i in psutil.process_iter()):
            call('taskkill.exe /F /IM ' + f_nam, shell=True)
    except ValueError:
        call('taskkill.exe /F /IM chrome.exe', shell=True)
    Popen(add_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)


cleanup()

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

if not os.path.isfile('./Essentials/VPN.txt') or len(open('./Essentials/VPN.txt', 'r').readlines()) == 0:
    open('./Essentials/VPN.txt', "w+")
    Sg.popup_error("Add vpn in the list !!!")
    call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
# ----------------------------------------------------------------------------------------------------------------------
if not os.path.isdir('C:/Program Files/OpenVPN'):
    if not os.path.isfile('./Essentials/OpenVPN.msi'):
        url = 'https://raw.githubusercontent.com/WoLvES-2x0/essential/main/OpenVPN.msi'
        open('./Essentials/OpenVPN.msi', 'wb').write((requests.get(url, headers=header)).content)
    call('%cd%\\Essentials\\OpenVPN.msi', shell=True)

url = 'https://raw.githubusercontent.com/WoLvES-2x0/essential/main/vpn-ip.csv'
vpn_ip_res = requests.get(url, headers=header)
vpn_raw = [i for i in base64.b64decode((g.get_user().get_repo('essential')).get_contents(
    parse.quote('vpn-raw.ovpn'), ref="main").content).decode("utf-8").split('\r') if i]
tk = [i for i in base64.b64decode((g.get_user().get_repo('essential')).get_contents(
    parse.quote('tk-ipinfo.txt'), ref="main").content).decode("utf-8").replace('\r', '').split('\n') if i]

img_data = b'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'


KILL_SWITCH = True

if auth:
    if not os.path.isfile(acc_f_path) or len(open(acc_f_path, 'r').readlines()) == 0:
        open(acc_f_path, "w+").write('0')

    MainIP = requests.get('https://api.ipify.org').text
    open('vi_f_path', 'w+').write(MainIP + '\n')
    cmd_x = 'netsh interface show interface | find "OpenVPN TAP-Windows6"'
    n_res = requests.get('https://raw.githubusercontent.com/WoLvES-2x0/essential/main/names.csv', headers=header)

    Vpn_Connected = False
    Vpn_change = False
    gender_switch_button = True
    Acc_Create = int(open(acc_f_path, 'r').readline().strip()) + 1
    TCP_SWITCH = True
    BROWSER_SWITCH = True
    test_connect2 = True
    ip_switch = False
    m_vpn_switch = False
    acc_no = 1

    def main_menu():
        global m_vpn_switch
        global Acc_Create
        global TCP_SWITCH
        global Vpn_Connected
        global BROWSER_SWITCH
        global gender_switch_button
        global ip_switch
        global KILL_SWITCH

        if not os.path.isfile('./Essentials/myauthfile.txt') or len(
                open('./Essentials/myauthfile.txt', 'r').readlines()) == 0:
            open('./Essentials/myauthfile.txt', 'w+')
            Sg.popup_error("Sign in!!")

        if not os.path.isfile('./Essentials/credentials.csv'):
            open("./Essentials/credentials.csv", "w+").write('mail,password,vpn')

        total_account = len(open('./Essentials/VPN.txt', 'r').readlines())

        def connecting_vpn():
            vpn_connect_thread = Thread(target=vpn_connect)
            vpn_connect_thread.start()
            if int(open(acc_f_path, 'r').readline().strip()) + 1 <= Acc_Create:
                Popen('"C:/Program Files/OpenVPN/bin/openvpn.exe" --auth-nocache --config ./Essentials/connect.ovpn',
                      shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        def start_function():
            cleanup()
            if m_vpn_switch:
                vpn_data_txt = open('./Essentials/VPN.txt', "r").readlines()
                vp_n = vpn_data_txt[int(open(acc_f_path, 'r').readline().strip())].replace('\n', '')
                cred_data_csv = pd.read_csv('./Essentials/credentials.csv', usecols=['vpn']).T.values.tolist()[0]
                if vp_n in cred_data_csv:
                    add_acc = int(open(acc_f_path, 'r').readline().strip()) + 1
                    open(acc_f_path, "w").write(str(add_acc))
                    start_function()
                else:
                    vpn_ip_csv = pd.read_csv(StringIO(vpn_ip_res.text), usecols=[vp_n.strip()]).T.values.tolist()[0]
                    vpn_ip = [x for x in vpn_ip_csv if not pd.isnull(x)]
                    vpn_raw_file = vpn_raw
                    if TCP_SWITCH:
                        vpn_raw_file[2] = "\nproto tcp"
                        vpn_raw_file[3] = "\nremote " + vpn_ip[0] + " 443"
                    if not TCP_SWITCH:
                        vpn_raw_file[2] = "\nproto udp"
                        vpn_raw_file[3] = '\nremote ' + vpn_ip[0] + ' 1194'
                    open('./Essentials/connect.ovpn', "w").writelines(vpn_raw_file)
                    connect_thread = Thread(target=connecting_vpn)
                    connect_thread.start()

        def start_process():
            global ip_switch
            global Acc_Create
            global Vpn_Connected
            global gender_switch_button
            global acc_no
            if Vpn_Connected:
                window['status'].update('Creating Acc: ' + str(acc_no))
                f_n_column = ''
                l_n_column = ''
                gender = 'male'

                if gender_switch_button:
                    gender = 'male'
                    f_n_column = 'Male First Name'
                    l_n_column = 'Male Last Name'
                if not gender_switch_button:
                    gender = 'female'
                    f_n_column = 'Female First Name'
                    l_n_column = 'Female Last Name'

                read_f_n = pd.read_csv(StringIO(n_res.text), usecols=[f_n_column]).T.values.tolist()[0]
                read_l_n = pd.read_csv(StringIO(n_res.text), usecols=[l_n_column]).T.values.tolist()[0]
                f_n = random.choice([x for x in read_f_n if not pd.isnull(x)])
                l_n = random.choice([x for x in read_l_n if not pd.isnull(x)])

                vpn_data_txt = open('./Essentials/VPN.txt', "r").readlines()
                v_n = vpn_data_txt[int(open(acc_f_path, "r").readline().strip())].replace('\n', '')
                str_var = list((''.join(
                    random.SystemRandom().choice(string.ascii_uppercase) for _ in range(random.randint(1, 2)))) + (
                                   ''.join(random.SystemRandom().choice(string.ascii_letters) for _ in
                                           range(random.randint(6, 8)))) + (
                                   ''.join(random.SystemRandom().choice(string.digits) for _ in
                                           range(random.randint(2, 4)))) + (
                                   ''.join(
                                       random.SystemRandom().choice('!@$%^*()') for _ in range(random.randint(1, 3)))))
                random.shuffle(str_var)
                p_a = ''.join(str_var)
                d_tn = datetime.now()
                var0 = getpass.getuser()
                var1 = str(d_tn.strftime("%m"))
                var2 = str(d_tn.strftime("%d"))
                var3 = str(d_tn.year)
                var4 = str(d_tn.strftime("%H"))
                var5 = str(d_tn.strftime("%M"))
                var6 = str(d_tn.strftime("%S"))
                var7 = p_a
                hsh = (hashlib.md5((var1 + var0 + var2 + var6 + var4 + var5 + var3 + var7).encode())).hexdigest()
                bser = str(BROWSER_SWITCH).lower()
                m_s = hsh + ',.,' + bser + ',.,' + gender + ',.,' + f_n + ',.,' + l_n + ',.,' + p_a + ',.,' + v_n
                base64_string = (base64.b64encode(m_s.encode('ascii'))).decode('ascii')
                acc_count01 = int(open(acc_f_path, 'r').readline().strip()) + 1
                if acc_count01 <= Acc_Create:
                    f_hash = ','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in [
                        i for i in glob.glob("*.exe") if i]])).split(',')
                    window['status'].update('Starting')
                    try:
                        m_file = f_hash[f_hash.index(file_hash) - 1]
                        if BROWSER_SWITCH:
                            call([m_file, base64_string], shell=True, start_new_session=True)
                        else:
                            Popen([m_file, base64_string], start_new_session=True)
                    except ValueError:
                        window['status'].update('File missing')
                window['status'].update('Done Creating Acc: ' + str(acc_no))
                acc_no = acc_no + 1
                open(acc_f_path, "w").write(str(acc_count01))
                curr_ip = requests.get('https://ipinfo.io/ip?token='+random.choice(tk)).text
                open(vi_f_path, 'a').write(curr_ip + '\n')
                if acc_count01 + 1 <= Acc_Create:
                    Vpn_Connected = False
                    ip_switch = True
                    if m_vpn_switch:
                        start_function()

        def ip_check_function():
            dc_switch = True
            while True:
                con_stat_arr = []
                for main_con in list(filter(None, str(
                        Popen('route print | find "0.0.0.0" | findstr /vc:"On-link"', shell=True, stdin=PIPE,
                              stdout=PIPE,
                              stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n'))):
                    con_stat_arr.append('0.0.0.0.0.0.0.0' in '.'.join(list(filter(None, main_con.split(' ')))))
                if not con_stat_arr:
                    restart_net()
                if False in con_stat_arr:
                    dc_switch = True
                    window.FindElement('Disconnect').Update(visible=True)
                    vpn_check()
                if dc_switch:
                    con_stat_arr = []
                    for main_con in list(filter(None, str(
                            Popen('route print | find "0.0.0.0" | findstr /vc:"On-link"', shell=True, stdin=PIPE,
                                  stdout=PIPE,
                                  stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n'))):
                        con_stat_arr.append('0.0.0.0.0.0.0.0' in '.'.join(list(filter(None, main_con.split(' ')))))
                    if not con_stat_arr:
                        restart_net()
                    if False not in con_stat_arr:
                        try:
                            time.sleep(3)
                            vpnip = requests.get('https://api.ipify.org').text
                            window['Current-IP'].Update("IP: " + format(vpnip))
                            window['Connect-Status'].Update('Status: Disconnected')
                            window['status'].update('Disconnected')
                            if vpnip == MainIP:
                                dc_switch = False
                        except requests.exceptions.ConnectionError:
                            window['status'].update('Waiting for Network to stabilize')

        ip_check_thread = Thread(target=ip_check_function)
        ip_check_thread.start()

        def vpn_connect():
            global Vpn_Connected
            n_switch = True
            gg = 1
            for _ in range(40):
                if m_vpn_switch:
                    con_stat_arr = []
                    for main_con in list(filter(None, str(
                            Popen('route print | find "0.0.0.0" | findstr /vc:"On-link"', shell=True, stdin=PIPE,
                                  stdout=PIPE,
                                  stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n'))):
                        con_stat_arr.append('0.0.0.0.0.0.0.0' in '.'.join(list(filter(None, main_con.split(' ')))))
                    if not con_stat_arr:
                        restart_net()
                    if False not in con_stat_arr:
                        time.sleep(1)
                        window['status'].update('Timeout: ' + str(gg))
                        gg += 1
                    con_stat_arr = []
                    for main_con in list(filter(None, str(
                            Popen('route print | find "0.0.0.0" | findstr /vc:"On-link"', shell=True, stdin=PIPE,
                                  stdout=PIPE,
                                  stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n'))):
                        con_stat_arr.append('0.0.0.0.0.0.0.0' in '.'.join(list(filter(None, main_con.split(' ')))))
                    if not con_stat_arr:
                        restart_net()
                    if False in con_stat_arr:
                        if n_switch:
                            window['status'].update('Connected')
                            n_switch = False

            con_stat_arr = []
            for main_con in list(filter(None, str(
                    Popen('route print | find "0.0.0.0" | findstr /vc:"On-link"', shell=True, stdin=PIPE,
                          stdout=PIPE,
                          stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n'))):
                con_stat_arr.append('0.0.0.0.0.0.0.0' in '.'.join(list(filter(None, main_con.split(' ')))))
            if not con_stat_arr:
                restart_net()
            if False not in con_stat_arr:
                window['status'].update('Error')
                if m_vpn_switch:
                    acc_count01 = int(open(acc_f_path, 'r').readline().strip()) + 1
                    if acc_count01 <= Acc_Create:
                        open(acc_f_path, "w").write(str(acc_count01))
                        Vpn_Connected = False
                        start_function()

        def vpn_check():
            global Vpn_Connected
            window['Connect-Status'].Update('Status: Connected')
            try:
                if not Vpn_Connected:
                    window['status'].update('Connected')
                    time.sleep(4)
                    current_ip = requests.get('https://ipinfo.io/ip?token='+random.choice(tk)).text
                    window['Current-IP'].Update("IP: " + current_ip)
                    if current_ip not in open(vi_f_path).read():
                        Popen(delete_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                        if not m_vpn_switch:
                            Popen(add_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                        Vpn_Connected = True
                        if int(open(acc_f_path, 'r').readline().strip()) + 1 <= Acc_Create:
                            start_process()
            except requests.exceptions.ConnectionError:
                window['status'].update('Waiting for Network to stabilize')

        Sg.theme('DarkBlack1')
        vpn_m_b = [[Sg.Button('TCP', size=(5, 1), button_color=('white', 'green'), key='_B_')]]
        g_button = [[Sg.Button('Male', size=(7, 1), button_color=('white', 'black'), key='-GENDER-SWITCH-')]]
        browser_b = [[Sg.Button('Browser', size=(10, 1), button_color=('white', 'green'), key='_Browser_')]]
        tab0_b = [[Sg.Button('Start', size=(6, 1))]]
        tab1_b = [[Sg.Button('Unlock', size=(6, 1))]]
        tab2_b = [[Sg.Button('Disconnect', size=(12, 1), visible=False)]]
        kill_switch_button = [[Sg.Button('K/S ON', size=(10, 1), button_color=('white', 'green'), key='Kill-Switch')]]

        layout_x = [[Sg.Text('Status: ', key='Connect-Status'), Sg.Text('IP :', key='Current-IP'),
                     Sg.Column(kill_switch_button, element_justification='r')],
                    [Sg.Text('Select how many account you want to Create.')],
                    [Sg.T(Acc_Create, size=(3, 1), key='_RIGHT_'),
                     Sg.Slider((Acc_Create, total_account), default_value=Acc_Create, key='_SLIDER_',
                               orientation='h', enable_events=True, size=(5, 0.4)), Sg.T(total_account, size=(3, 1))],
                    [Sg.Column(g_button, element_justification='l'), Sg.Column(vpn_m_b, element_justification='l'),
                     Sg.Column(browser_b, element_justification='r')],
                    [Sg.Column(tab2_b, element_justification='l'), Sg.Column(tab1_b, element_justification='c'),
                     Sg.Column(tab0_b, element_justification='r')]]

        layout = [[Sg.Column(layout_x)],
                  [Sg.Text("", size=(20, 0.5), font='Any 8', key='status')]]
        window = Sg.Window("Create Accounts!!", layout, icon=img_data, resizable=False, finalize=True)

        while True:
            event, values = window.Read()
            if event is None or event == 'Exit':
                m_vpn_switch = False
                cleanup()
                call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
                break

            elif event == 'Disconnect':
                m_vpn_switch = False
                cleanup()

            elif event == 'Kill-Switch':
                KILL_SWITCH = not KILL_SWITCH
                window.Element('Kill-Switch').Update(('K/S OFF', 'K/S ON')[KILL_SWITCH],
                                                     button_color=('white', ('gray', 'green')[KILL_SWITCH]))

            elif event == '-GENDER-SWITCH-':
                gender_switch_button = not gender_switch_button
                window.Element('-GENDER-SWITCH-').Update(('Female', 'Male')[gender_switch_button], button_color=(
                    'white', ('gray', 'black')[gender_switch_button]))

            elif event == '_B_':
                TCP_SWITCH = not TCP_SWITCH
                window.Element('_B_').Update(('UDP', 'TCP')[TCP_SWITCH],
                                             button_color=('white', ('gray', 'green')[TCP_SWITCH]))

            elif event == '_Browser_':
                BROWSER_SWITCH = not BROWSER_SWITCH
                window.Element('_Browser_').Update(('No Browser', 'Browser')[BROWSER_SWITCH],
                                                   button_color=('white', ('gray', 'green')[BROWSER_SWITCH]))

            elif event == 'Start':
                window.FindElement('_B_').Update(disabled=True)
                window.FindElement('Start').Update(disabled=True)
                window.FindElement('_SLIDER_').Update(disabled=True)
                window.FindElement('_Browser_').Update(disabled=True)
                if int(open(acc_f_path, 'r').readline().strip()) <= Acc_Create:
                    Vpn_Connected = False
                    ip_switch = True
                    m_vpn_switch = True
                    start_function()

            elif event == 'Unlock':
                window.FindElement('_B_').Update(disabled=False)
                window.FindElement('Start').Update(disabled=False)
                window.FindElement('_SLIDER_').Update(disabled=False)
                window.FindElement('_Browser_').Update(disabled=False)

            window.Element('_RIGHT_').Update(values['_SLIDER_'])
            Acc_Create = int(values['_SLIDER_'])

        window.Close()


    main_menu_thread_x = Thread(target=main_menu)
    main_menu_thread_x.start()


def ip_check_function_x():
    global KILL_SWITCH
    switch = True
    while True:
        if KILL_SWITCH:
            con_stat_arr = []
            for main_con in list(filter(None, str(
                    Popen('route print | find "0.0.0.0" | findstr /vc:"On-link"', shell=True, stdin=PIPE,
                          stdout=PIPE,
                          stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n'))):
                con_stat_arr.append('0.0.0.0.0.0.0.0' in '.'.join(list(filter(None, main_con.split(' ')))))
            if not con_stat_arr:
                restart_net()
            if False not in con_stat_arr:
                if switch:
                    Popen(add_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    switch = False
                f_hash = ','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in [
                    i for i in glob.glob("*.exe") if i]])).split(',')
                try:
                    f_name = f_hash[f_hash.index(file_hash) - 1]
                    if f_name in (i.name() for i in psutil.process_iter()):
                        call('taskkill.exe /F /IM ' + f_name, shell=True)
                except ValueError:
                    call('taskkill.exe /F /IM chrome.exe', shell=True)
            else:
                switch = True


ip_check_thread_x = Thread(target=ip_check_function_x)
ip_check_thread_x.start()

if not auth:
    call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
