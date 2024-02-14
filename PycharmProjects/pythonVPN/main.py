import _cffi_backend
import base64
from io import StringIO
from threading import Thread
from urllib import parse

import PySimpleGUIQt as Sg
import getpass
import ntpath
import os
import pandas as pd
import psutil
import requests
import smtplib
import ssl
from subprocess import PIPE, Popen, call
import time
from requests import get
from github import Github

auth = True
add_route = ''
delete_route = ''
call('taskkill.exe /F /IM openvpn.exe', shell=True)


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


hw_id = str(
    Popen('wmic csproduct get uuid', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()[0]
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


username = ''
password = ''
line_count = ''
test = ''
sentence = ''

array2 = []
array = []
country = []
filename4 = []

thread_ip_check = True
kill_switch_tf = True
TCP_SWITCH = True
kill_switch_button = True
test_connect = False
test_connect2 = True

if auth:
    if not os.path.isdir('./Essentials/'):
        os.mkdir('./Essentials/')
    if not os.path.isfile('./Essentials/theme.txt') or len(open('./Essentials/theme.txt', 'r').readlines()) == 0:
        open("./Essentials/theme.txt", "w+").write('BlueMono')

    g = Github("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")
    header = {"Authorization": "token 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",
              "Accept": "application/vnd.github.v4.raw"}
    server_list = base64.b64decode((g.get_user().get_repo('essential')).get_contents(
        parse.quote('servers.csv'), ref="main").content).decode("utf-8").replace('\r', '')
    vpn_ip_list = base64.b64decode((g.get_user().get_repo('essential')).get_contents(
        parse.quote('vpn-ip.csv'), ref="main").content).decode("utf-8").replace('\r', '')
    vpn_raw = base64.b64decode((g.get_user().get_repo('essential')).get_contents(
        parse.quote('vpn-raw.ovpn'), ref="main").content).decode("utf-8").split('\r')
    if not os.path.isdir('C:/Program Files/OpenVPN'):
        if not os.path.isfile('./Essentials/OpenVPN.msi'):
            url = 'https://raw.githubusercontent.com/WoLvES-2x0/essential/main/OpenVPN.msi'
            open('./Essentials/OpenVPN.msi', 'wb').write((requests.get(url, headers=header)).content)
        call('%cd%\\Essentials\\OpenVPN.msi', shell=True)

    img_data = b'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'
    themes = open('./Essentials/theme.txt', 'r').readline().strip()

    for f in Sg.theme_list():
        if themes == f:
            sentence = themes

    country = (server_list.split('\n'))[0].split(',')


    def main_vpn(theme=sentence):
        if theme:
            Sg.theme(theme)
        global country
        global array
        global array2
        global filename4
        global kill_switch_button
        global kill_switch_tf
        global thread_ip_check
        global TCP_SWITCH
        global test
        global test_connect
        global test_connect2
        ip2 = get('https://api.ipify.org').text
        vpnip = ip2

        def threaded_function():
            Popen('"C:/Program Files/OpenVPN/bin/openvpn.exe" --auth-nocache --config ./Essentials/connect.ovpn',
                  shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        def threaded_connecting():
            global test_connect
            time.sleep(30)
            test_connect = False

        def threaded_ip_check():
            global thread_ip_check
            global test_connect

            while thread_ip_check:
                if not thread_ip_check:
                    break
                if test_connect:
                    window["-ip-vpn-connect-"].Update("Connecting")
                    con_stat_arr = []
                    for main_con in list(filter(None, str(
                            Popen('route print | find "0.0.0.0" | findstr /vc:"On-link"', shell=True, stdin=PIPE,
                                  stdout=PIPE,
                                  stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n'))):
                        con_stat_arr.append('0.0.0.0.0.0.0.0' in '.'.join(list(filter(None, main_con.split(' ')))))
                    if False in con_stat_arr:
                        vpn_connect()
                        time.sleep(30)
                        test_connect = False
                if not test_connect:
                    con_stat_arr = []
                    for main_con in list(filter(None, str(
                            Popen('route print | find "0.0.0.0" | findstr /vc:"On-link"', shell=True, stdin=PIPE,
                                  stdout=PIPE,
                                  stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n'))):
                        con_stat_arr.append('0.0.0.0.0.0.0.0' in '.'.join(list(filter(None, main_con.split(' ')))))
                    if not con_stat_arr:
                        restart_net()
                    if False in con_stat_arr:
                        vpn_connect()
                    else:
                        vpn_disconnect_auto()

        def threaded_ip_check2():
            global kill_switch_tf
            global array2
            while kill_switch_tf:
                if not kill_switch_tf:
                    break
                con_stat_arr = []
                for main_con in list(filter(None, str(
                        Popen('route print | find "0.0.0.0" | findstr /vc:"On-link"', shell=True, stdin=PIPE,
                              stdout=PIPE,
                              stderr=PIPE).communicate()[0].decode("utf-8")).replace('\r', '').split('\n'))):
                    con_stat_arr.append('0.0.0.0.0.0.0.0' in '.'.join(list(filter(None, main_con.split(' ')))))
                if not con_stat_arr:
                    restart_net()

                if False not in con_stat_arr:
                    if array2:
                        for x_test in array2:
                            kill_switch(x_test)

        ip_check_2: Thread = Thread(target=threaded_ip_check2)
        ip_check_2.start()

        def vpn_connect2():
            global test_connect2
            time.sleep(3)
            if test_connect2:
                Popen(delete_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                test_connect2 = False

        def vpn_connect():
            global test_connect
            test_connect = False
            time.sleep(1)
            window["-ip-vpn-connect-"].Update("Connected")
            window["DISCONNECT"].update(visible=True)
            vpn_connect2_thread: Thread = Thread(target=vpn_connect2)
            vpn_connect2_thread.start()
            try:
                vpn_ip_add = get('https://api.ipify.org').text
                window["-ip-vpn-"].Update("Your current IP: " + format(vpn_ip_add))
            except requests.exceptions.ConnectionError:
                vpn_ip_add = "Getting IP"
                window["-ip-vpn-"].Update("Your current IP: " + vpn_ip_add)

        def vpn_disconnect_auto():
            global test_connect2
            time.sleep(1)
            window["-ip-vpn-connect-"].Update("Not Connected")
            window["DISCONNECT"].update(visible=False)
            test_connect2 = True
            try:
                vpn_ip_add = get('https://api.ipify.org').text
                window["-ip-vpn-"].Update("Your current IP: " + format(vpn_ip_add))
            except requests.exceptions.ConnectionError:
                vpn_ip_add = "Getting IP"
                window["-ip-vpn-"].Update("Your current IP: " + vpn_ip_add)

        def kill_switch(x_test):
            if kill_switch_button:
                After_process_search = "".join([s for s in x_test.strip().splitlines(True) if s.strip("\r\n").strip()])
                process_search = After_process_search in (i.name() for i in psutil.process_iter())
                if process_search:
                    call('taskkill.exe /F /IM ' + x_test, shell=True)

        curr_theme = open('./Essentials/theme.txt', 'r').readline().strip().replace('\n', '')

        vpn_info = [[Sg.Text("Your Original IP: " + format(ip2))],
                    [Sg.Text(("Your current IP: " + format(vpnip)), key="-ip-vpn-")],
                    [Sg.Text("Not Connected", key="-ip-vpn-connect-")]]
        Country_names = [[Sg.Listbox(values=country, enable_events=True, select_mode=Sg.LISTBOX_SELECT_MODE_SINGLE,
                                     size=(20, 10), key="-FILE LIST-")]]
        server_names = [[Sg.Listbox(values=[], enable_events=True, select_mode=Sg.LISTBOX_SELECT_MODE_SINGLE,
                                    size=(20, 10), key="-TOUT-", visible=False)]]
        con_b = [[Sg.Button("CONNECT", size=(8, 1), visible=False)]]
        d_con_b = [[Sg.Button("DISCONNECT", size=(10, 1), visible=False), ]]
        tcp_udp_combo = [[Sg.Button('TCP', size=(5, 1), button_color=('white', 'green'), key='_B_')]]
        tab1_layout = [[Sg.Column(vpn_info)],
                       [Sg.Column(tcp_udp_combo), Sg.Column(con_b, element_justification='r')],
                       [Sg.Column(Country_names), Sg.Column(server_names)],
                       [Sg.Column(d_con_b, element_justification='r')]]
        tab2_layout = [[Sg.Text("Kill Switch:", justification='l', font='Any 15'),
                        Sg.Button('ON', size=(5, 1), button_color=('white', 'green'), key='_Kill-Switch_')],
                       [Sg.Listbox(values=[], enable_events=True, size=(22, 10),
                                   select_mode=Sg.LISTBOX_SELECT_MODE_SINGLE, visible=True, key="-APP-LIST-")],
                       [Sg.Input(size=(10, 1), enable_events=True, key='-ADD-APP-', visible=False),
                        Sg.FileBrowse(size=(22, 1))], [Sg.Button("DELETE", disabled=True, size=(22, 1))]]
        tab3_layout = [[Sg.Text("Themes", justification='c', font='Any 15')],
                       [Sg.Text("Current Theme: " + curr_theme, justification='l', font='Any 10')],
                       [Sg.Listbox(values=Sg.theme_list(), enable_events=True, size=(20, 14),
                                   select_mode=Sg.LISTBOX_SELECT_MODE_SINGLE, key="-THEME-")]]
        tab_group_layout = [[Sg.Tab('VPN Tab', tab1_layout, font='Courier 15', key='-TAB1-'),
                             Sg.Tab('Kill Switch', tab2_layout, visible=True, key='-TAB2-'),
                             Sg.Tab('Theme', tab3_layout, visible=True, key='-TAB3-')]]
        layout = [[Sg.Menu([['&File', ['&Login']], ['&Edit', ['&Settings'], ], ['&Help', '&About...'], ])],
                  [Sg.TabGroup(tab_group_layout, enable_events=True, key='-TABGROUP-')]]

        window = Sg.Window("NordVPN", layout, icon=img_data, resizable=False, finalize=True)
        ip_check: Thread = Thread(target=threaded_ip_check)
        ip_check.start()
        try:
            clean = "".join(line for line in open("./Essentials/taskkill.txt") if not line.isspace())
            open("./Essentials/taskkill.txt", 'w+').write(clean)
            array2.clear()
            for tk in open("./Essentials/taskkill.txt").readlines():
                array2.append(tk.replace("\n", ""))
            window["-APP-LIST-"].Update(array2)
        except FileNotFoundError:
            open("./Essentials/taskkill.txt", "w+")

        while True:
            event, values = window.read()

            if event == "DISCONNECT":
                global test_connect
                window["DISCONNECT"].update(visible=False)
                test_connect = False
                call('taskkill.exe /F /IM openvpn.exe', shell=True)
                window["-ip-vpn-connect-"].Update("Not Connected")
                vpnip = "Getting IP"
                window["-ip-vpn-"].Update("Your current IP: " + vpnip)
                Popen(add_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

            elif event == "Login":
                login()

            if event == Sg.WIN_CLOSED:
                thread_ip_check = False
                kill_switch_tf = False
                call('taskkill.exe /F /IM openvpn.exe', shell=True)
                Popen(add_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                call('wmic path win32_networkadapter where PhysicalAdapter=True call disable',
                     shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                call('wmic path win32_networkadapter where PhysicalAdapter=True call enable',
                     shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)

            if event == '_B_':
                TCP_SWITCH = not TCP_SWITCH
                window.Element('_B_').Update(('UDP', 'TCP')[TCP_SWITCH],
                                             button_color=('white', ('red', 'green')[TCP_SWITCH]))

            if event == '_Kill-Switch_':
                kill_switch_button = not kill_switch_button
                window.Element('_Kill-Switch_').Update(('OFF', 'ON')[kill_switch_button],
                                                       button_color=('white', ('red', 'green')[kill_switch_button]))

            elif event == "-FILE LIST-":
                filename = values["-FILE LIST-"]
                window["-TOUT-"].update(visible=True)
                servers = server_list
                server_csv = pd.read_csv(StringIO(servers), usecols=[filename[0]]).T.values.tolist()[0]
                array = [z for z in server_csv if not pd.isnull(z)]
                window["-TOUT-"].Update(array)

            elif event == "-TOUT-":
                filename4 = values["-TOUT-"]
                window["CONNECT"].update(visible=True)

            elif event == "CONNECT":
                Popen(add_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                call('taskkill.exe /F /IM openvpn.exe', shell=True)
                vpn_csv = vpn_ip_list
                vpn_ip_csv = pd.read_csv(StringIO(vpn_csv), usecols=[filename4[0]]).T.values.tolist()[0]
                vpn_ip = [z for z in vpn_ip_csv if not pd.isnull(z)]
                vpn_raw_file = vpn_raw
                if TCP_SWITCH:
                    vpn_raw_file[2] = "\nproto tcp"
                    vpn_raw_file[3] = "\nremote " + vpn_ip[0] + " 443"
                if not TCP_SWITCH:
                    vpn_raw_file[2] = "\nproto udp"
                    vpn_raw_file[3] = "\nremote" + vpn_ip[0] + " 1194"
                open('./Essentials/connect.ovpn', "w").writelines(vpn_raw_file)
                test_connect = True
                test_connect2 = True
                thread_con = Thread(target=threaded_connecting)
                thread_con.start()
                co_con = Thread(target=threaded_function)
                co_con.start()

            elif event == "-ADD-APP-":
                try:
                    App_name = ntpath.basename(values['-ADD-APP-'])
                    tk_array_clean_0 = [i.replace('\n', '') for i in open("./Essentials/taskkill.txt").readlines()]
                    if App_name not in tk_array_clean_0:
                        open("./Essentials/taskkill.txt", "a").write(App_name + "\n")
                    clean = "".join(line for line in open("./Essentials/taskkill.txt") if not line.isspace())
                    open("./Essentials/taskkill.txt", 'w+').write(clean)
                    array2 = [i.replace('\n', '') for i in open("./Essentials/taskkill.txt").readlines()]
                    window["-APP-LIST-"].Update(array2)

                except FileNotFoundError:
                    pass
            elif event == "-APP-LIST-":
                window["DELETE"].Update(disabled=False)

            elif event == "DELETE":
                if values["-APP-LIST-"]:
                    array2.remove(values["-APP-LIST-"][0].strip())
                    window["-APP-LIST-"].Update(array2)
                    open('./Essentials/taskkill.txt', 'w').write('\n'.join(array2))
                    window["DELETE"].Update(disabled=True)

            elif event == "-THEME-":
                theme = values["-THEME-"][0]
                open("./Essentials/theme.txt", "w").write(theme + "\n")
                window.close()
                main_vpn(theme)


    def login(theme=sentence):
        global username, password, line_count
        if theme:
            Sg.theme(theme)

        login_button = [[Sg.Button("Login", size=(10, 1), visible=True)]]
        layout = [[Sg.Text("Log In", justification='center', font='Any 25')],
                  [Sg.Text("Username", size=(10, 1), font='Any 15'),
                   Sg.InputText(key='-usrnm-', size=(21, 1), font='Any 15')],
                  [Sg.Text("Password", size=(10, 1), font='Any 15'),
                   Sg.InputText(key='-pwd-', password_char='*', size=(21, 1), font='Any 15')],
                  [Sg.Column(login_button, element_justification='r')]]

        window = Sg.Window("Change Log In", layout, icon=img_data, default_element_size=(15, 1),
                           resizable=False, grab_anywhere=True, no_titlebar=False)

        while True:
            event, values = window.read()
            if event == Sg.WIN_CLOSED:
                exit()
            elif event == "Login":
                open("./Essentials/myauthfile.txt", "w").write(values['-usrnm-'] + "\n")
                open("./Essentials/myauthfile.txt", "a").write(values['-pwd-'] + "\n")
                Sg.popup("Username and Password Updated...")
                break
        window.close()


    def auth_file():
        while True:
            if not os.path.isfile('./Essentials/myauthfile.txt'):
                open('./Essentials/myauthfile.txt', 'w+')
            if len(open('./Essentials/myauthfile.txt', 'r').readlines()) < 2:
                login()
            elif len(open('./Essentials/myauthfile.txt', 'r').readlines()) == 2:
                main_vpn()
                break


    auth_line: Thread = Thread(target=auth_file)
    auth_line.start()

if not auth:
    call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
