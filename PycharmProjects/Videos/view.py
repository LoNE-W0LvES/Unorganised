import _cffi_backend
import base64
import getpass
import glob
import hashlib
import os
import smtplib
import ssl
from subprocess import call, Popen, PIPE
import time
from datetime import datetime
from io import StringIO
from threading import Thread
from urllib import parse
import random

import PySimpleGUIQt as Sg
import pandas as pd
import psutil
import requests
from github import Github

time_str = time.strftime("%d-%m-%Y")
auth = False

if not os.path.isdir('./Essentials/tempview/'):
    if not os.path.isdir('./Essentials/'):
        os.mkdir('./Essentials/')
    os.mkdir('./Essentials/tempview/')

acc_f_path = './Essentials/tempview/' + time_str + '.txt'
vi_f_path = './Essentials/UsedIPs.txt'
auth_loc = './Essentials/myauthfile.txt'
id_loc = './Essentials/ID.txt'
cred_f_path = './Essentials/credentials.csv'

add_route = ''
delete_route = ''


def restart_net():
    global add_route
    global delete_route
    network_rs = True
    if 'openvpn.exe' in (i.name() for i in psutil.process_iter()):
        call('taskkill.exe /F /IM openvpn.exe', shell=True)
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
file_hash = node_hash[node_hash.index('view') + 1]


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


if not os.path.isfile(cred_f_path) or len(open(cred_f_path, 'r').readlines()) == 0:
    open(cred_f_path, 'w+')
    Sg.popup_error("Add accounts !!!")
    call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)

########################################################################################################################

if not os.path.isdir('C:/Program Files/OpenVPN'):
    if not os.path.isfile('./Essentials/OpenVPN.msi'):
        url = 'https://raw.githubusercontent.com/WoLvES-2x0/essential/main/OpenVPN.msi'
        open('./Essentials/OpenVPN.msi', 'wb').write((requests.get(url, headers=header)).content)
    call('%cd%\\Essentials\\OpenVPN.msi', shell=True)

url = 'https://raw.githubusercontent.com/WoLvES-2x0/essential/main/vpn-ip.csv'
vpn_ip_response = requests.get(url, headers=header)
vpn_raw = [i for i in base64.b64decode((g.get_user().get_repo('essential')).get_contents(
    parse.quote('vpn-raw.ovpn'), ref="main").content).decode("utf-8").split('\r') if i]
tk = [i for i in base64.b64decode((g.get_user().get_repo('essential')).get_contents(
    parse.quote('tk-ipinfo.txt'), ref="main").content).decode("utf-8").replace('\r', '').split('\n') if i]

img_data = b'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'

KILL_SWITCH = True
if auth:

    if not os.path.isfile(acc_f_path) or len(open(acc_f_path, 'r').readlines()) == 0:
        open(acc_f_path, "w+").write('0')

    total_acc = len(open(cred_f_path, 'r').readlines()) - 1

    Vpn_Connected = False
    Vpn_change = False
    Acc_Create = int(open(acc_f_path, 'r').readline().strip()) + 1
    TCP_SWITCH = True
    BROWSER_SWITCH = True
    Acc_At_a_Time = 1
    Timer_value = 31
    Slider_play_value = 6
    test_connect2 = True
    m_vpn_switch = False

    if Acc_Create > total_acc:
        Sg.popup('No More account left!!')
        call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)

    diff = total_acc + 1 - Acc_Create

    at_t = diff if (diff < 10) else 10

    def main_menu():
        global Acc_Create
        global TCP_SWITCH
        global Timer_value
        global Vpn_Connected
        global Acc_At_a_Time
        global BROWSER_SWITCH
        global m_vpn_switch

        if not os.path.isfile(auth_loc) or len(open(auth_loc, 'r').readlines()) == 0:
            open(auth_loc, 'w+')
            Sg.popup_error("Sign in!!")

        if not os.path.isfile(id_loc) or len(open(id_loc, 'r').readlines()) == 0:
            open(id_loc, "w+")
            Sg.popup_error("Add Accounts links!!!")

        def connecting_vpn():
            if int(open(acc_f_path, 'r').readline().strip()) < Acc_Create:
                window['status'].update('Connecting vpn')
                Popen('"C:/Program Files/OpenVPN/bin/openvpn.exe" --auth-nocache --config ./Essentials/connect.ovpn',
                      shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        def start_function():
            global test_connect2
            if m_vpn_switch:
                test_connect2 = True
                window['status'].update('Restarting network')
                cleanup()
                Popen(add_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                vpn_data = pd.read_csv(cred_f_path, usecols=['vpn']).T.values.tolist()[0]
                vpn_name = vpn_data[int(open(acc_f_path, 'r').readline().strip())]
                v_i_c = pd.read_csv(StringIO(vpn_ip_response.text), usecols=[vpn_name.strip()]).T.values.tolist()[0]
                vpn_ip = [x for x in v_i_c if not pd.isnull(x)]
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
                vpn_connect_thread = Thread(target=vpn_connect)
                vpn_connect_thread.start()

        def open_node(base64_string):
            window['status'].update('Starting')
            if int(open(acc_f_path, "r").readline().strip()) <= Acc_Create:
                f_hah = ','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in [
                    i for i in glob.glob("*.exe") if i]])).split(',')
                try:
                    f_name = f_hah[f_hah.index(file_hash) - 1]
                    if BROWSER_SWITCH:
                        call([f_name, base64_string], shell=True)
                    else:
                        call([f_name, base64_string], start_new_session=True)
                except ValueError:
                    window['status'].update('File missing')

        def lookout():
            if int(open(acc_f_path, 'r').readline().strip()) >= total_acc:
                window['status'].update('Max Account reached')
                cleanup()

        lookout_thread = Thread(target=lookout)
        lookout_thread.start()

        def start_process():
            global Acc_Create
            global Acc_At_a_Time
            global Vpn_Connected
            global Timer_value
            global Slider_play_value
            global m_vpn_switch
            window['status'].update('Getting ready')
            if Vpn_Connected:
                d = {}
                for i in range(0, Acc_At_a_Time):
                    acc_pos = int(open(acc_f_path, 'r').readline().strip())
                    mail_data = pd.read_csv(cred_f_path, usecols=['mail']).T.values.tolist()[0]
                    pass_data = pd.read_csv(cred_f_path, usecols=['password']).T.values.tolist()[0]
                    id_list = open('./Essentials/ID.txt', 'r').readlines()
                    ids = id_list[acc_pos].replace('\n', '')
                    mail = mail_data[acc_pos].replace('\n', '')
                    pss = pass_data[acc_pos].replace('\n', '')
                    t_v = str(Timer_value * 1000)
                    s_p = str(Slider_play_value)
                    d_tn = datetime.now()
                    var0 = getpass.getuser()
                    var1 = str(d_tn.strftime("%m"))
                    var2 = str(d_tn.strftime("%d"))
                    var3 = str(d_tn.year)
                    var4 = str(d_tn.strftime("%H"))
                    var5 = str(d_tn.strftime("%M"))
                    var6 = str(d_tn.strftime("%S"))
                    var7 = pss
                    hsh = (hashlib.md5((var3 + var5 + var4 + var2 + var1 + var6 + var7 + var0).encode())).hexdigest()
                    bser = str(BROWSER_SWITCH).lower()
                    main_s = hsh + ',.,' + t_v + ',.,' + s_p + ',.,' + bser + ',.,' + mail + ',.,' + pss + ',.,' + ids
                    base64_string = base64.b64encode(main_s.encode('ascii')).decode('ascii')

                    if int(open(acc_f_path, 'r').readline().strip()) + 1 <= Acc_Create:
                        d["call_sub_thread{0}".format(i)] = Thread(target=open_node, args=(base64_string,))
                for z in range(0, Acc_At_a_Time):
                    d["call_sub_thread{0}".format(z)].start()
                    time.sleep(1)
                for y in range(0, Acc_At_a_Time):
                    d["call_sub_thread{0}".format(y)].join()

                acc_add = int(open(acc_f_path, 'r').readline().strip()) + Acc_At_a_Time
                open(acc_f_path, 'w').write(str(acc_add))

                f_hsh = ','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in [
                    i for i in glob.glob("*.exe") if i]])).split(',')
                try:
                    f_nme = f_hsh[f_hsh.index(file_hash) - 1]
                    if f_nme in (i.name() for i in psutil.process_iter()):
                        call('taskkill.exe /F /IM ' + f_nme, shell=True)
                except ValueError:
                    call('taskkill.exe /F /IM chrome.exe', shell=True)
                curr_ip = requests.get('https://ipinfo.io/ip?token='+random.choice(tk)).text
                open(vi_f_path, "a").write(curr_ip + '\n')
                call('taskkill.exe /F /IM openvpn.exe', shell=True)
                Popen(add_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                if int(open(acc_f_path, 'r').readline().strip()) + 1 <= Acc_Create:
                    Vpn_Connected = False
                    start_function()

        main_ip = requests.get('https://api.ipify.org').text
        open(vi_f_path, "w").write(main_ip + '\n')

        def vpn_connect():
            global Vpn_Connected
            global m_vpn_switch
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

        def ip_check_function():
            dc_switch = True
            global test_connect2
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
                    test_connect2 = True
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
                            test_connect2 = True
                            time.sleep(3)
                            vpnip = requests.get('https://api.ipify.org').text
                            window['Current-IP'].Update("IP: " + format(vpnip))
                            if vpnip == main_ip:
                                dc_switch = False
                        except requests.exceptions.ConnectionError:
                            pass
                        window.FindElement('Disconnect').Update(visible=False)
                        window['Connect-Status'].Update('Status: Disconnected')
                        window['status'].update('Disconnected')

        ip_check_thread = Thread(target=ip_check_function)
        ip_check_thread.start()

        def vpn_check():
            global test_connect2
            global Vpn_Connected
            if test_connect2:
                Popen(delete_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                if not m_vpn_switch:
                    Popen(add_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                test_connect2 = False
            window['Connect-Status'].Update('Status: Connected')
            try:
                if not Vpn_Connected:
                    window['status'].update('Connected')
                    currt_ip = requests.get('https://ipinfo.io/ip?token='+random.choice(tk)).text
                    window['Current-IP'].Update("IP: " + currt_ip)
                    if currt_ip not in open(vi_f_path).read():
                        Vpn_Connected = True
                        if int(open(acc_f_path, 'r').readline().strip()) + 1 <= Acc_Create:
                            time.sleep(5)
                            start_process()
            except requests.exceptions.ConnectionError:
                pass

        global KILL_SWITCH
        Sg.theme('DarkBlack1')
        vpn_m_b = [[Sg.Button('TCP', size=(5, 1), button_color=('white', 'green'), key='_B_')]]
        bro_b = [[Sg.Button('Browser', size=(10, 1), button_color=('white', 'green'), key='_Browser_')]]
        tab0_button = [[Sg.Button('Start', size=(6, 1))]]
        tab1_b = [[Sg.Button('Unlock', size=(6, 1))]]
        tab2_b = [[Sg.Button('Disconnect', size=(12, 1), visible=False)]]
        kill_switch_button = [[Sg.Button('K/S ON', size=(10, 1), button_color=('white', 'green'), key='Kill-Switch')]]
        tab0_layout = [[Sg.Text('Status: ', key='Connect-Status'), Sg.Text('IP :', key='Current-IP'),
                        Sg.Column(kill_switch_button, element_justification='r')],
                       [Sg.Text('Select how many account you want to use.')],
                       [Sg.T(Acc_Create, key='_RIGHT_'),
                        Sg.Slider((Acc_Create, total_acc), default_value=Acc_Create, key='_SLIDER_', orientation='h',
                                  enable_events=True, size=(5, 0.4)), Sg.T(total_acc)],
                       [Sg.Text("Select how many account you want to open at once.")],
                       [Sg.T('1', key='_RIGHT1_'),
                        Sg.Slider((1, at_t), default_value=1, key='_SLIDER_AAT_', orientation='h', enable_events=True,
                                  size=(5, 0.4)), Sg.T(at_t)], [Sg.Text("Select How many videos you want to play")],
                       [Sg.T('6', key='_RIGHT_play_'),
                        Sg.Slider((1, 20), default_value=6, key='_SLIDER_play_',
                                  orientation='h', enable_events=True, size=(5, 0.4)), Sg.T('20')],
                       [Sg.Text("Per video watch time")],
                       [Sg.T('31', key='_RIGHT2_'),
                        Sg.Slider((31, 60), default_value=31, key='_SLIDER_SEC_',
                                  orientation='h', enable_events=True, size=(5, 0.4)), Sg.T('60')],
                       [Sg.Column(vpn_m_b, element_justification='l'), Sg.Column(bro_b, element_justification='r')],
                       [Sg.Column(tab2_b, element_justification='l'), Sg.Column(tab1_b, element_justification='c'),
                        Sg.Column(tab0_button, element_justification='r')]]

        layout = [[Sg.Column(tab0_layout)],
                  [Sg.Text("", size=(20, 0.5), font='Any 8', key='status')]]
        window = Sg.Window("View", layout, icon=img_data, resizable=False, finalize=True)

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

            elif event == '_B_':
                TCP_SWITCH = not TCP_SWITCH
                window.Element('_B_').Update(('UDP', 'TCP')[TCP_SWITCH],
                                             button_color=('white', ('gray', 'green')[TCP_SWITCH]))

            elif event == '_Browser_':
                BROWSER_SWITCH = not BROWSER_SWITCH
                window.Element('_Browser_').Update(('No Browser', 'Browser')[BROWSER_SWITCH],
                                                   button_color=('white', ('gray', 'green')[BROWSER_SWITCH]))

            elif event == 'Start':
                if Acc_At_a_Time <= total_acc:
                    window.FindElement('_B_').Update(disabled=True)
                    window.FindElement('Start').Update(disabled=True)
                    window.FindElement('_SLIDER_').Update(disabled=True)
                    window.FindElement('_Browser_').Update(disabled=True)
                    window.FindElement('_SLIDER_AAT_').Update(disabled=True)
                    if int(open(acc_f_path, 'r').readline().strip()) <= Acc_Create:
                        Vpn_Connected = False
                        test_connect2 = True
                        m_vpn_switch = True
                        start_function()

            elif event == 'Unlock':
                window.FindElement('_B_').Update(disabled=False)
                window.FindElement('Start').Update(disabled=False)
                window.FindElement('_SLIDER_').Update(disabled=False)
                window.FindElement('_Browser_').Update(disabled=False)
                window.FindElement('_SLIDER_AAT_').Update(disabled=False)
            window.Element('_RIGHT_').Update(values['_SLIDER_'])
            Acc_Create = int(values['_SLIDER_'])
            window.Element('_RIGHT2_').Update(values['_SLIDER_SEC_'])
            Timer_value = values['_SLIDER_SEC_']
            window.Element('_RIGHT_play_').Update(values['_SLIDER_play_'])
            Slider_play_value = values['_SLIDER_play_']
            window.Element('_RIGHT1_').Update(values['_SLIDER_AAT_'])
            Acc_At_a_Time = values['_SLIDER_AAT_']

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
