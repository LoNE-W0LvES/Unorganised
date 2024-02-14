# import dns.resolver
# res = dns.resolver.Resolver(configure=False)
# res.nameservers = ['8.8.4.4']
# answer = res.query('google.com', 'ns')
# print(answer)
#
# for i in answer:
#     print(i)


# from pydnserver import DNSServer
#
# ip = u'192.168.31.195'  # Set this to the IP address of your network interface.
#
# dns = DNSServer(interface=ip, port=53)
# dns.start()
#
# try:
#     while True:
#         pass
#
# except KeyboardInterrupt:
#     dns.stop()
import os
from requests import get
import requests
import subprocess
OpenVPN_version_web = get('https://pastebin.com/raw/fj9GursP').text
if not os.path.isfile('./Essentials/OpenVPN-version.txt'):
    open("./Essentials/OpenVPN-version.txt", "w+")
    with open("./Essentials/OpenVPN-version.txt", "w") as fileOpenVPN:
        fileOpenVPN.write(OpenVPN_version_web)
        fileOpenVPN.close()

with open('./Essentials/OpenVPN-version.txt', 'r') as file1:
    OpenVPN_version_text = file1.readline().strip()
    file1.close()

if not OpenVPN_version_web == OpenVPN_version_text:
    with open("./Essentials/OpenVPN-version.txt", "w") as file8:
        file8.write(OpenVPN_version_web)
        file8.close()
    urlx = 'https://swupdate.openvpn.org/community/releases/' + OpenVPN_version_web
    r = requests.get(urlx, allow_redirects=True)
    open('./Essentials/OpenVPN.msi', 'wb').write(r.content)

if not os.path.isfile('./Essentials/OpenVPN.msi'):
    with open("./Essentials/OpenVPN-version.txt", "w") as file9:
        file9.write(OpenVPN_version_web)
        file9.close()
    urlx = 'https://swupdate.openvpn.org/community/releases/' + OpenVPN_version_web
    r = requests.get(urlx, allow_redirects=True)
    open('./Essentials/OpenVPN.msi', 'wb').write(r.content)
if os.path.isdir('C:/Program Files/OpenVPN'):
    subprocess.call('%cd%\\Essentials\\OpenVPN.msi', shell=True)

# -----------------------------------------------------------------------------------------------
import PySimpleGUIQt as Sg
import requests, os, time, ntpath, psutil, csv, subprocess, smtplib, ssl, getpass, uuid
from requests import get
from threading import Thread
import pandas as pd

auth = False

# subprocess.call("wmic path win32_networkadapter where PhysicalAdapter=True call disable", shell=True)
# subprocess.call("wmic path win32_networkadapter where PhysicalAdapter=True call enable", shell=True)

network_test = 'test network'
data_test = requests.get('https://pastebin.com/raw/kTWQnSx4').text
if network_test in data_test:
    network_test_success = True

pc_username = getpass.getuser()
hwid = str(uuid.uuid1(uuid.getnode(), 0))[24:]

data = requests.get('https://pastebin.com/raw/y9e52zB6').text
data1 = requests.get('https://raw.githubusercontent.com/W0LvES-2-0/vuser/main/user.txt').text
if hwid in data:
    auth = True
elif hwid in data1:
    auth = True
else:
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "w3961500@gmail.com"
    receiver_email = "wolvesbatch1@gmail.com"
    password = "wolvesbatch00"
    message = pc_username + '\n' + hwid

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    Sg.popup("Wait for Verification")
    self_pid = str(os.getpid())
    os.system("taskkill /F /PID " + self_pid)
    subprocess.call('taskkill.exe /F /IM ' + self_pid, shell=True)

subprocess.call('taskkill.exe /F /IM openvpn.exe', shell=True)
username = ''
password = ''
line_count = ''
test = ''
sentence = ''

array2 = []
array = []
countrys = []
vpnip = []

thread_ipcheck = True
kill_switchtf = True
TCP_SWITCH = True
kill_switch_button = True
test_connect = False
test_connect2 = True
if auth:
    if not os.path.isdir('./Essentials/'):
        os.mkdir('./Essentials/')

    # ----------------------------------------SERVER VERSION------------------------------------------
    server_version_web = get('https://pastebin.com/raw/ZSc3YgzY').text
    if not os.path.isfile('./Essentials/servers-version.txt'):
        open("./Essentials/servers-version.txt", "w+")
        with open("./Essentials/servers-version.txt", "w") as file2:
            file2.write(server_version_web)
            file2.close()

    with open('./Essentials/servers-version.txt', 'r') as file1:
        servers_version_text = file1.readline().strip()
        file1.close()

    if not server_version_web == servers_version_text:
        with open("./Essentials/servers-version.txt", "w") as file8:
            file8.write(server_version_web)
            file8.close()
        url = 'https://cdn.discordapp.com/attachments/' + server_version_web + '/servers.csv'
        r = requests.get(url, allow_redirects=True)
        open('./Essentials/servers.csv', 'wb').write(r.content)

    if not os.path.isfile('./Essentials/servers.csv'):
        with open("./Essentials/servers-version.txt", "w") as file9:
            file9.write(server_version_web)
            file9.close()
        url = 'https://cdn.discordapp.com/attachments/' + server_version_web + '/servers.csv'
        r = requests.get(url, allow_redirects=True)
        open('./Essentials/servers.csv', 'wb').write(r.content)
    # ----------------------------------------SERVER VERSION------------------------------------------

    # ----------------------------------------OpenVPN VERSION------------------------------------------
    OpenVPN_version_web = get('https://pastebin.com/raw/fj9GursP').text
    if not os.path.isfile('./Essentials/OpenVPN-version.txt'):
        open("./Essentials/OpenVPN-version.txt", "w+")
        with open("./Essentials/OpenVPN-version.txt", "w") as fileOpenVPN:
            fileOpenVPN.write(OpenVPN_version_web)
            fileOpenVPN.close()

    with open('./Essentials/OpenVPN-version.txt', 'r') as file1:
        OpenVPN_version_text = file1.readline().strip()
        file1.close()

    if not OpenVPN_version_web == OpenVPN_version_text:
        with open("./Essentials/OpenVPN-version.txt", "w") as file8:
            file8.write(OpenVPN_version_web)
            file8.close()
        urlx = 'https://swupdate.openvpn.org/community/releases/' + OpenVPN_version_web
        r = requests.get(urlx, allow_redirects=True)
        open('./Essentials/OpenVPN.msi', 'wb').write(r.content)

    if not os.path.isfile('./Essentials/OpenVPN.msi'):
        with open("./Essentials/OpenVPN-version.txt", "w") as file9:
            file9.write(OpenVPN_version_web)
            file9.close()
        urlx = 'https://swupdate.openvpn.org/community/releases/' + OpenVPN_version_web
        r = requests.get(urlx, allow_redirects=True)
        open('./Essentials/OpenVPN.msi', 'wb').write(r.content)
    if not os.path.isdir('C:/Program Files/OpenVPN'):
        subprocess.call('%cd%\\Essentials\\OpenVPN.msi', shell=True)

    # ----------------------------------------OpenVPN VERSION------------------------------------------

    # ----------------------------------------VPN IP VERSION------------------------------------------
    vpn_ip_version_web = get('https://pastebin.com/raw/CGFh4WMi').text
    if not os.path.isfile('./Essentials/vpn-ip-version.txt'):
        open("./Essentials/vpn-ip-version.txt", "w+")
        with open("./Essentials/vpn-ip-version.txt", "w") as file4:
            file4.write(vpn_ip_version_web)
            file4.close()

    with open('./Essentials/vpn-ip-version.txt', 'r') as file5:
        vpn_ip_version_text = file5.readline().strip()
        file5.close()

    if not vpn_ip_version_web == vpn_ip_version_text:
        with open("./Essentials/vpn-ip-version.txt", "w") as file6:
            file6.write(vpn_ip_version_web)
            file6.close()

        url1 = 'https://cdn.discordapp.com/attachments/' + vpn_ip_version_web + '/vpnip.csv'
        r = requests.get(url1, allow_redirects=True)
        open('./Essentials/vpnip.csv', 'wb').write(r.content)

    if not os.path.isfile('./Essentials/vpnip.csv'):
        with open("./Essentials/vpn-ip-version.txt", "w") as file7:
            file7.write(vpn_ip_version_web)
            file7.close()
        url1 = 'https://cdn.discordapp.com/attachments/' + vpn_ip_version_web + '/vpnip.csv'
        r = requests.get(url1, allow_redirects=True)
        open('./Essentials/vpnip.csv', 'wb').write(r.content)

    # ----------------------------------------VPN IP VERSION------------------------------------------

    # ----------------------------------------VPN connect VERSION------------------------------------------
    vpn_connect_version_web = get('https://pastebin.com/raw/Bse9RbvB').text
    if not os.path.isfile('./Essentials/vpn-connect-version.txt'):
        open("./Essentials/vpn-connect-version.txt", "w+")
        with open("./Essentials/vpn-connect-version.txt", "w") as file11:
            file11.write(vpn_connect_version_web)
            file11.close()

    with open('./Essentials/vpn-connect-version.txt', 'r') as file12:
        vpn_connect_version_text = file12.readline().strip()
        file12.close()

    if not vpn_connect_version_web == vpn_connect_version_text:
        with open("./Essentials/vpn-connect-version.txt", "w") as file13:
            file13.write(vpn_connect_version_web)
            file13.close()

        url2 = 'https://cdn.discordapp.com/attachments/' + vpn_connect_version_web + '/vpnraw.ovpn'
        r = requests.get(url2, allow_redirects=True)
        open('./Essentials/vpnraw.ovpn', 'wb').write(r.content)

    if not os.path.isfile('./Essentials/vpnraw.ovpn'):
        with open("./Essentials/vpn-connect-version.txt", "w") as file14:
            file14.write(vpn_connect_version_web)
            file14.close()
        url2 = 'https://cdn.discordapp.com/attachments/' + vpn_connect_version_web + '/vpnraw.ovpn'
        r = requests.get(url2, allow_redirects=True)
        open('./Essentials/vpnraw.ovpn', 'wb').write(r.content)

    # ----------------------------------------VPN connect VERSION------------------------------------------

    if not os.path.isfile('./Essentials/app.ico'):
        urlico = 'https://cdn.discordapp.com/attachments/862321604490690562/871869106301845514/app.ico'
        r = requests.get(urlico, allow_redirects=True)
        open('./Essentials/app.ico', 'wb').write(r.content)

    if not os.path.isfile('./Essentials/theme.txt'):
        open("./Essentials/theme.txt", "w+")

    with open('./Essentials/theme.txt', 'r') as file3:
        theme1 = file3.readline().strip()
        file3.close()

    for f in Sg.theme_list():
        if theme1 == f:
            sentence = theme1

    with open('./Essentials/servers.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                countrys = row
                line_count += 1


    def main_vpn(theme=sentence):
        if theme:
            Sg.theme(theme)
        global countrys
        global array
        global array2
        global vpnip
        global kill_switch_button
        global kill_switchtf
        global thread_ipcheck
        global TCP_SWITCH
        global test
        global test_connect
        global test_connect2
        ip2 = get('https://api.ipify.org').text
        vpnip = ip2

        def threaded_function():
            subprocess.call(
                "\"C:/Program Files/OpenVPN/bin/openvpn.exe\" --auth-nocache --config ./Essentials/connect.ovpn",
                shell=True)

        def threaded_connecting():
            global test_connect
            time.sleep(30)
            test_connect = False

        def threaded_ip_check():
            global thread_ipcheck
            global test_connect

            while thread_ipcheck:
                test_vpn_con = subprocess.call(
                    'netsh interface show interface | find \"Connected\" | find \"OpenVPN TAP-Windows6\"', shell=True)
                testing = str(test_vpn_con)
                if not thread_ipcheck:
                    break
                if test_connect:
                    window["-ip-vpn-connect-"].Update("Connecting")
                    if testing == '0':
                        vpn_connect()
                        time.sleep(30)
                        test_connect = False
                if not test_connect:
                    if testing == '0':
                        vpn_connect()
                    elif testing == '1':
                        vpn_disconnectauto()

        ipcheck: Thread = Thread(target=threaded_ip_check)
        ipcheck.start()

        def threaded_ipcheck2():
            global kill_switchtf
            global array2
            while kill_switchtf:
                test_vpn_con1 = subprocess.call(
                    'netsh interface show interface | find \"Connected\" | find \"OpenVPN TAP-Windows6\"', shell=True)
                testing1 = str(test_vpn_con1)
                if kill_switchtf:
                    break
                if testing1 == '1':
                    for x_test in array2:
                        kill_switch(x_test)

        ipcheck_2: Thread = Thread(target=threaded_ipcheck2)
        ipcheck_2.start()

        def vpn_connect2():
            global test_connect2
            time.sleep(5)
            if test_connect2:
                subprocess.call('route delete 0.0.0.0', shell=True)
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
                vpnip = get('https://api.ipify.org').text
                window["-ip-vpn-"].Update("Your current IP: " + format(vpnip))
            except:
                vpnip = "Getting IP"
                window["-ip-vpn-"].Update("Your current IP: " + vpnip)

        def vpn_disconnectauto():
            global test_connect2
            time.sleep(1)
            window["-ip-vpn-connect-"].Update("Not Connected")
            window["DISCONNECT"].update(visible=False)
            test_connect2 = True
            try:
                vpnip = get('https://api.ipify.org').text
                window["-ip-vpn-"].Update("Your current IP: " + format(vpnip))
            except:
                vpnip = "Getting IP"
                window["-ip-vpn-"].Update("Your current IP: " + vpnip)

        def network_restart_connect():
            subprocess.call("wmic path win32_networkadapter where PhysicalAdapter=True call disable", shell=True)
            subprocess.call("wmic path win32_networkadapter where PhysicalAdapter=True call enable", shell=True)
            thread = Thread(target=threaded_function)
            thread.start()

        def kill_switch(x_test):
            if kill_switch_button:
                After_process_search = "".join([s for s in x_test.strip().splitlines(True) if s.strip("\r\n").strip()])
                process_search = After_process_search in (i.name() for i in psutil.process_iter())
                if process_search:
                    subprocess.call('taskkill.exe /F /IM ' + x_test, shell=True)
                else:
                    pass
            else:
                pass

        vpn_info = [
            [
                Sg.Text("Your Original IP: " + format(ip2))
            ],
            [
                Sg.Text(
                    ("Your current IP: " + format(vpnip)), key="-ip-vpn-"
                )
            ],
            [
                Sg.Text(
                    "Not Connected", key="-ip-vpn-connect-"
                )
            ],
        ]

        Country_names = [
            [
                Sg.Listbox(
                    values=countrys, enable_events=True, select_mode=Sg.LISTBOX_SELECT_MODE_SINGLE, size=(20, 10),
                    key="-FILE LIST-"
                )
            ],
        ]

        server_names = [
            [

                Sg.Listbox(
                    values=[], enable_events=True, size=(20, 10), visible=False,
                    key="-TOUT-"
                ),
            ],
        ]

        con_btest = [
            [Sg.Button("CONNECT", size=(8, 1), visible=False), ]
        ]

        dcon_btest = [
            [Sg.Button("DISCONNECT", size=(10, 1), visible=False), ]
        ]

        tcpudp_combo = [

            [
                Sg.Button('TCP', size=(5, 1), button_color=('white', 'green'), key='_B_')
            ],

        ]

        tab1_layout = [
            [
                Sg.Column(vpn_info),
            ],
            [
                Sg.Column(tcpudp_combo), Sg.Column(con_btest, element_justification='r')
            ],
            [
                Sg.Column(Country_names),
                Sg.Column(server_names),
            ],
            [Sg.Column(dcon_btest, element_justification='r')]
        ]

        tab2_layout = [
            [
                Sg.Text("Kill Switch:", justification='l', font='Any 15'),
                Sg.Button('ON', size=(5, 1), button_color=('white', 'green'), key='_Kill-Switch_')
            ],
            [
                Sg.Listbox(
                    values=[], enable_events=True, size=(22, 10), visible=True,
                    key="-APP-LIST-"
                ),
            ],
            [
                Sg.Input(size=(10, 1), enable_events=True, key='-ADD-APP-', visible=False), Sg.FileBrowse(size=(22, 1))
            ],
            [
                Sg.Button("ADD", size=(22, 1))
            ],
            [
                Sg.Button("DELETE", size=(22, 1)),

            ]
        ]

        tab3_layout = [
            [
                Sg.Text("Themes", justification='c', font='Any 15'),
            ],
            [
                Sg.Listbox(values=Sg.theme_list(), enable_events=True, size=(22, 14), key="-THEME-")
            ]
        ]

        tab_group_layout = [[Sg.Tab('VPN Tab', tab1_layout, font='Courier 15', key='-TAB1-'),
                             Sg.Tab('Kill Switch', tab2_layout, visible=True, key='-TAB2-'),
                             Sg.Tab('Theme', tab3_layout, visible=True, key='-TAB3-'),
                             ]]

        layout = [
            [Sg.Menu([['&File', ['&Login']], ['&Edit', ['&Settings'], ], ['&Help', '&About...'], ])],
            [Sg.TabGroup(tab_group_layout, enable_events=True, key='-TABGROUP-')],
        ]

        window = Sg.Window("NORD VPN", layout, icon='./Essentials/app.ico', resizable=False, finalize=True)

        # try:
        #     with open("./Essentials/taskkill.txt", 'r+') as fd:
        #         lines = fd.readlines()
        #         fd.seek(0)
        #         fd.writelines(line for line in lines if line.strip())
        #         fd.truncate()
        #         fd.close()
        #         with open("./Essentials/taskkill.txt") as file:
        #             array2raw = file.readlines()
        #             file.close()
        #             array2.clear()
        #         for x in array2raw:
        #             array2.append(x.replace("\n", ""))
        #     window["-APP-LIST-"].Update(array2)
        #
        # except:
        #     open("./Essentials/taskkill.txt", "a")

        while True:

            event, values = window.read()

            if event == "DISCONNECT":
                global test_connect
                test_connect = False
                subprocess.call('taskkill.exe /F /IM openvpn.exe', shell=True)
                window["-ip-vpn-connect-"].Update("Not Connected")
                vpnip = "Getting IP"
                window["-ip-vpn-"].Update("Your current IP: " + vpnip)
                subprocess.call("wmic path win32_networkadapter where PhysicalAdapter=True call disable", shell=True)
                subprocess.call("wmic path win32_networkadapter where PhysicalAdapter=True call enable", shell=True)

            elif event == "Login":
                try:
                    login()
                except:
                    pass
            if event == Sg.WIN_CLOSED:
                thread_ipcheck = False
                kill_switchtf = False
                subprocess.call('taskkill.exe /F /IM openvpn.exe', shell=True)
                subprocess.call("wmic path win32_networkadapter where PhysicalAdapter=True call disable", shell=True)
                subprocess.call("wmic path win32_networkadapter where PhysicalAdapter=True call enable", shell=True)
                pid_self = str(os.getpid())
                subprocess.call('taskkill.exe /F /IM ' + pid_self, shell=True)

            if event == '_B_':
                TCP_SWITCH = not TCP_SWITCH
                window.Element('_B_').Update(('UDP', 'TCP')[TCP_SWITCH],
                                             button_color=(('white', ('red', 'green')[TCP_SWITCH])))

            if event == '_Kill-Switch_':
                kill_switch_button = not kill_switch_button
                window.Element('_Kill-Switch_').Update(('OFF', 'ON')[kill_switch_button],
                                                       button_color=(('white', ('red', 'green')[kill_switch_button])))

            elif event == "-FILE LIST-":

                try:
                    filename = values["-FILE LIST-"]
                    window["-TOUT-"].update(visible=True)
                    data = pd.read_csv('./Essentials/servers.csv', usecols=[filename[0]]).T.values.tolist()[0]
                    array = [x for x in data if pd.isnull(x) == False]
                    window["-TOUT-"].Update(array)
                except:
                    pass

            elif event == "-TOUT-":
                try:
                    filename4 = values["-TOUT-"]
                    data1 = pd.read_csv('./Essentials/vpnip.csv', usecols=[filename4[0]]).T.values.tolist()[0]
                    vpnip = [x for x in data1 if pd.isnull(x) == False]

                    window["CONNECT"].update(visible=True)
                except:
                    pass

            elif event == "CONNECT":
                network_restart_thread = Thread(target=network_restart_connect)
                network_restart_thread.start()
                subprocess.call('taskkill.exe /F /IM openvpn.exe', shell=True)
                a_file = open("./Essentials/vpnraw.ovpn", "r")
                list_of_lines = a_file.readlines()
                if TCP_SWITCH:
                    list_of_lines[2] = "proto tcp\n"
                    list_of_lines[3] = "remote " + vpnip[0] + " 443\n"
                if not TCP_SWITCH:
                    list_of_lines[2] = "proto udp\n"
                    list_of_lines[3] = "remote" + vpnip[0] + " 1194\n"
                a_file = open('./Essentials/connect.ovpn', "w")
                a_file.writelines(list_of_lines)
                a_file.close()
                test_connect = True
                test_connect2 = True
                thread_con = Thread(target=threaded_connecting)
                thread_con.start()

            elif event == "ADD":
                try:
                    App_name = ntpath.basename(values['-ADD-APP-'])
                    array2 = open("./Essentials/taskkill.txt").readlines()
                    if not (len(list(filter(lambda x: x == App_name + '\n', array2))) > 0):
                        open("./Essentials/taskkill.txt", "a").write(App_name + "\n")

                    with open("./Essentials/taskkill.txt", 'r+') as fd:
                        lines = fd.readlines()
                        fd.seek(0)
                        fd.writelines(line for line in lines if line.strip())
                        fd.truncate()
                        fd.close()

                    array2.clear()
                    for y in open("./Essentials/taskkill.txt").readlines():
                        array2.append(y.replace("\n", ""))
                    window["-APP-LIST-"].Update(array2)
                except:
                    pass

            elif event == "DELETE":
                App_list = values["-APP-LIST-"]
                app_from_list = App_list[0].strip()
                bad_words = [app_from_list]
                task_array = open('./Essentials/taskkill.txt').readlines()
                task_array.remove(app_from_list)
                print(task_array)

                with open('./Essentials/taskkill.txt') as oldfile, open('./Essentials/newtaskkill.txt', 'w') as newfile:
                    for line in oldfile:
                        if not any(bad_word in line for bad_word in bad_words):
                            newfile.write(line)
                if os.path.isfile("./Essentials/taskkill.txt"):
                    os.remove("./Essentials/taskkill.txt")
                    if os.path.isfile("./Essentials/newtaskkill.txt"):
                        os.rename('./Essentials/newtaskkill.txt', './Essentials/taskkill.txt')
                    else:
                        pass
                else:
                    pass
                with open("./Essentials/taskkill.txt") as file:
                    array2 = file.readlines()
                    file.close()
                window["-APP-LIST-"].Update(array2)


            elif event == "-THEME-":
                theme = values["-THEME-"][0]
                open("./Essentials/theme.txt", "w").write(theme + "\n")
                window.close()
                main_vpn(theme)

        # window.close()


    def login(theme=sentence):
        global username, password, line_count
        if theme:
            Sg.theme(theme)

        login_button = [
            [Sg.Button("Login", size=(10, 1), visible=True), ]
        ]
        layout = [[Sg.Text("Log In", justification='center', font='Any 25')],
                  [Sg.Text("Username", size=(10, 1), font='Any 15'),
                   Sg.InputText(key='-usrnm-', size=(21, 1), font='Any 15')],
                  [Sg.Text("Password", size=(10, 1), font='Any 15'),
                   Sg.InputText(key='-pwd-', password_char='*', size=(21, 1), font='Any 15')],
                  [Sg.Column(login_button, element_justification='r')]
                  ]

        window = Sg.Window("Change Log In", layout, icon='./Essentials/app.ico', default_element_size=(15, 1), resizable=False, grab_anywhere=True,
                           no_titlebar=False)

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
    self_pid = str(os.getpid())
    subprocess.call('taskkill.exe /F /IM ' + self_pid, shell=True)