import math

import _cffi_backend
import getpass
import glob
import hashlib
import os
import smtplib
import ssl
import threading
from subprocess import call, Popen, PIPE
from time import monotonic

import PySimpleGUI as Sg
import psutil
import requests
from github import Github
import time
from math import floor

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
    g = Github("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")
    header = {"Authorization": "token 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",
              "Accept": "application/vnd.github.v4.raw"}
    ####################################################################################################################
    if not os.path.isdir('./Videos/waiting for upload/'):
        if not os.path.isdir('./Videos/'):
            os.mkdir('./Videos/')
        os.mkdir('./Videos/waiting for upload/')

    if not os.path.isdir('./Essentials/tempview/'):
        if not os.path.isdir('./Essentials/'):
            os.mkdir('./Essentials/')
        os.mkdir('./Essentials/tempview/')
    if not os.path.isfile('./Essentials/VPN.txt') or len(open('./Essentials/VPN.txt', 'r').readlines()) == 0:
        open('./Essentials/VPN.txt', "w+")
    if not os.path.isdir('C:/Program Files/OpenVPN'):
        if not os.path.isfile('./Essentials/OpenVPN.msi') or math.ceil(
                os.path.getsize('./Essentials/OpenVPN.msi')/1048576) < 1:
            url = 'https://raw.githubusercontent.com/WoLvES-2x0/essential/main/OpenVPN.msi'
            open('./Essentials/OpenVPN.msi', 'wb').write((requests.get(url, headers=header)).content)
        call('%cd%\\Essentials\\OpenVPN.msi', shell=True)
    if not os.path.isfile('./Essentials/myauthfile.txt') or len(
            open('./Essentials/myauthfile.txt', 'r').readlines()) == 0:
        open('./Essentials/myauthfile.txt', 'w+')
    if not os.path.isfile('./Essentials/credentials.csv'):
        open("./Essentials/credentials.csv", "w+").write('mail,password,vpn')
    if not os.path.isfile('./Essentials/ID.txt') or len(open('./Essentials/ID.txt', 'r').readlines()) == 0:
        open('./Essentials/ID.txt', "w+")
    acc_cred = './Essentials/main-acc.txt'
    vid_desc = './Essentials/description.txt'
    if not os.path.isfile(acc_cred) or len(open(acc_cred, 'r').readlines()) == 0:
        open('./Essentials/main-acc.txt', 'w+')
        Sg.popup("Add main account!!")
    if not os.path.isfile(vid_desc) or len(open(vid_desc, 'r').readlines()) == 0:
        open('./Essentials/description.txt', 'w+')
        Sg.popup_error("Add upload video Description!!")
    ####################################################################################################################

    g_p_f_name = [str(i).replace('ContentFile(path="', '').replace('")', '') for i in
                  (g.get_user().get_repo('python-files')).get_contents('') if i]
    git_p_hf = ' '.join(map(str, g_p_f_name)).lower().split(' ')
    link_head = 'https://raw.githubusercontent.com/WoLvES-2x0/python-files/main/'
    link_tag = "{0}{1}".format(link_head, [i for i in g_p_f_name if 'addtags' in i.lower()][0])
    link_upload = "{0}{1}".format(link_head, [i for i in g_p_f_name if 'upload' in i.lower()][0])
    link_create = "{0}{1}".format(link_head, [i for i in g_p_f_name if 'create' in i.lower()][0])
    link_view = "{0}{1}".format(link_head, [i for i in g_p_f_name if 'view' in i.lower()][0])

    g_n_f_name = [str(i).replace('ContentFile(path="', '').replace('")', '') for i in
                  (g.get_user().get_repo('node-files')).get_contents('') if i]
    git_n_hf = ' '.join(map(str, g_n_f_name)).lower().split(' ')
    link_n_head = 'https://raw.githubusercontent.com/WoLvES-2x0/node-files/main/'
    link_n_tag = ''
    link_n_upload = "{0}{1}".format(link_n_head, [i for i in g_n_f_name if 'upload' in i.lower()][0])
    link_n_create = "{0}{1}".format(link_n_head, [i for i in g_n_f_name if 'create' in i.lower()][0])
    link_n_view = "{0}{1}".format(link_n_head, [i for i in g_n_f_name if 'view' in i.lower()][0])

    links = [link_tag, link_upload, link_create, link_view]
    n_links = [link_n_tag, link_n_upload, link_n_create, link_n_view]
    python_names = ['tags-part1.exe', 'upload-part1.exe', 'create-part1.exe', 'view-part1.exe']
    node_names = ['tags-part2.exe', 'upload-part2.exe', 'create-part2.exe', 'view-part2.exe']
    just_name = ['Tag', 'Upload', 'Create', 'View']
    tags_name = ''
    upload_name = ''
    create_name = ''
    view_name = ''
    p_array = []
    tags_n_name = ''
    upload_n_name = ''
    create_n_name = ''
    view_n_name = ''
    n_array = []
    img_data = b'iVBORw0KGgoAAAANSUhEUgAAADAAAAAyCAYAAAAayliMAAAACXBIWXMAAAsTAAALEwEAmpwYAAAFF2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNy4wLWMwMDAgNzkuMjE3YmNhNiwgMjAyMS8wNi8xNC0xODoyODoxMSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iIHhtbG5zOnBob3Rvc2hvcD0iaHR0cDovL25zLmFkb2JlLmNvbS9waG90b3Nob3AvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIDIyLjQgKFdpbmRvd3MpIiB4bXA6Q3JlYXRlRGF0ZT0iMjAyMS0wOC0yNVQxNTo1Njo1NiswNjowMCIgeG1wOk1vZGlmeURhdGU9IjIwMjEtMDgtMjVUMTc6Mzc6MjYrMDY6MDAiIHhtcDpNZXRhZGF0YURhdGU9IjIwMjEtMDgtMjVUMTc6Mzc6MjYrMDY6MDAiIGRjOmZvcm1hdD0iaW1hZ2UvcG5nIiBwaG90b3Nob3A6Q29sb3JNb2RlPSIzIiBwaG90b3Nob3A6SUNDUHJvZmlsZT0ic1JHQiBJRUM2MTk2Ni0yLjEiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6YzI2ODdhMTgtZTk2Zi0x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'


    def download_file(link, file_name, k):
        r = requests.get(link, headers=header, stream=True)
        file_size = int(r.headers['content-length'])
        ceil_value = floor(file_size / 100)
        downloaded = 0
        start = monotonic()
        with open(file_name, 'wb') as fp:
            for chunk in r.iter_content(chunk_size=ceil_value):
                downloaded += fp.write(chunk)
                now = monotonic()
                c_out = round(downloaded / file_size * 100)

                window.write_event_value(f'Next{k}', c_out)
                window[f'speed{k}'].update('S: ' + f'{round(downloaded / (now - start) / 1024) / 1024:.2f}' +
                                           " MBps  D: " + f'{round(downloaded / 1024) / 1024:.2f}' + " MB",
                                           font='any 8')


    def test_thread():
        global tags_name
        global upload_name
        global create_name
        global view_name
        global p_array
        global n_array
        global tags_n_name
        global upload_n_name
        global create_n_name
        global view_n_name
        while True:
            files_hash = ','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in
                                            [i for i in glob.glob("*.exe") if i]])).split(',')
            tags_hash = git_p_hf[git_p_hf.index('addtags') + 1]
            upload_hash = git_p_hf[git_p_hf.index('upload') + 1]
            create_hash = git_p_hf[git_p_hf.index('create') + 1]
            view_hash = git_p_hf[git_p_hf.index('view') + 1]
            upload_n_hash = git_n_hf[git_n_hf.index('upload') + 1]
            create_n_hash = git_n_hf[git_n_hf.index('create') + 1]
            view_n_hash = git_n_hf[git_n_hf.index('view') + 1]
            window['Download-node0'].update(visible=False)
            window['space0'].update('                                                ')

            if tags_hash not in files_hash:
                window['Download0'].update('Download')
                window['Launch0'].update(disabled=True)
            else:
                window['Download0'].update('Re-Download')
                tags_name = files_hash[files_hash.index(tags_hash) - 1]
                if tags_name not in (i.name() for i in psutil.process_iter()):
                    window['Launch0'].update(disabled=False)
                    window['Close0'].update(disabled=True)
                else:
                    window['Launch0'].update(disabled=True)
                    window['Close0'].update(disabled=False)

            if upload_hash not in files_hash:
                window['Download1'].update('Download')
            else:
                upload_name = files_hash[files_hash.index(upload_hash) - 1]
                window['Download1'].update('Re-Download')

            if upload_n_hash not in files_hash:
                window['Download-node1'].update('Download')
            else:
                upload_n_name = files_hash[files_hash.index(upload_n_hash) - 1]
                window['Download-node1'].update('Re-Download')

            if create_hash not in files_hash:
                window['Download2'].update('Download')
            else:
                create_name = files_hash[files_hash.index(create_hash) - 1]
                window['Download2'].update('Re-Download')

            if create_n_hash not in files_hash:
                window['Download-node2'].update('Download')
            else:
                create_n_name = files_hash[files_hash.index(create_n_hash) - 1]
                window['Download-node2'].update('Re-Download')

            if view_hash not in files_hash:
                window['Download3'].update('Download')
            else:
                view_name = files_hash[files_hash.index(view_hash) - 1]
                window['Download3'].update('Re-Download')

            if view_n_hash not in files_hash:
                window['Download-node3'].update('Download')
            else:
                view_n_name = files_hash[files_hash.index(view_n_hash) - 1]
                window['Download-node3'].update('Re-Download')

            if upload_hash not in files_hash or upload_n_hash not in files_hash:
                window['Launch1'].update(disabled=True)
            else:
                if upload_name not in (i.name() for i in psutil.process_iter()) or upload_n_name not in (
                        i.name() for i in psutil.process_iter()):
                    window['Launch1'].update(disabled=False)
                    window['Close1'].update(disabled=True)
                else:
                    window['Launch1'].update(disabled=True)
                    window['Close1'].update(disabled=False)

            if create_hash not in files_hash or create_n_hash not in files_hash:
                window['Launch2'].update(disabled=True)
            else:
                if create_name not in (i.name() for i in psutil.process_iter()) or create_n_name not in (
                        i.name() for i in psutil.process_iter()):
                    window['Launch2'].update(disabled=False)
                    window['Close2'].update(disabled=True)
                else:
                    window['Launch2'].update(disabled=True)
                    window['Close2'].update(disabled=False)

            if view_hash not in files_hash or view_n_hash not in files_hash:
                window['Launch3'].update(disabled=True)
            else:
                if view_name not in (i.name() for i in psutil.process_iter()) or view_n_name not in (
                        i.name() for i in psutil.process_iter()):
                    window['Launch3'].update(disabled=False)
                    window['Close3'].update(disabled=True)
                else:
                    window['Launch3'].update(disabled=True)
                    window['Close3'].update(disabled=False)
            p_array = [tags_name, upload_name, create_name, view_name]
            n_array = [tags_n_name, upload_n_name, create_n_name, view_n_name]
            time.sleep(1)


    Sg.theme("DarkBlue")
    layout_x = []
    login_layout = [[Sg.Text("                             Log In                             ", font='Any 25')],
                    [Sg.Text(" ")],
                    [Sg.Text("Username", size=(10, 1), font='Any 15')],
                    [Sg.InputText(key='-usrnm-', font='Any 15')],
                    [Sg.Text(" ")],
                    [Sg.Text("Password", size=(10, 1), font='Any 15')],
                    [Sg.InputText(key='-pwd-', password_char='*', font='Any 15')],
                    [Sg.Text(" ")],
                    [Sg.Button("Save", size=(10, 1), visible=True)]]
    for j in range(len(links)):
        layout_x += [[Sg.Text(just_name[j], font='any 15')],
                     [Sg.Button('Download', size=(15, 1), key=f'Download{j}'),
                      Sg.Button('Download', size=(15, 1), key=f'Download-node{j}'),
                      Sg.Text("              ", key=f'space{j}'),
                      Sg.Button('Launch', size=(15, 1), key=f'Launch{j}'),
                      Sg.Button('Close', size=(15, 1), disabled=True, key=f'Close{j}')],
                     [Sg.ProgressBar(100, size=(40, 1), pad=(0, 0), key=f'ProBar{j}'),
                      Sg.Text("  0%", size=(4, 1), font='any 8', key=f'Percent{j}'),
                      Sg.Text("", visible=False, font='any 8', key=f'speed{j}')]]

    tab_g_l = [[Sg.Tab('                                  Menu                                 ',
                       layout_x, font='Courier 15', key='-TAB1-'),
                Sg.Tab('                               VPN Login                               ',
                       login_layout, visible=True, key='-TAB2-')]]

    layout = [[Sg.TabGroup(tab_g_l, title_color='#0f0f0f', enable_events=True, key='-TAB0-')],
              [Sg.Text("", size=(20, 1), font='Any 8', key='status')]]

    window = Sg.Window('Launcher', layout, icon=img_data, use_default_focus=False, resizable=False, finalize=True)
    thread_x = threading.Thread(target=test_thread)
    thread_x.start()

    while True:
        event, values = window.read()
        if event == Sg.WINDOW_CLOSED:
            call('taskkill.exe /F /IM openvpn.exe', shell=True)
            Popen(add_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            call('wmic path win32_networkadapter where PhysicalAdapter=True call disable',
                 shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            call('wmic path win32_networkadapter where PhysicalAdapter=True call enable',
                 shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
            break
        for j in range(len(links)):
            if event == f'Download{j}':
                window[f'Download{j}'].update(disabled=True)
                window[f'Download-node{j}'].update(disabled=True)
                window[f'Percent{j}'].update("  0%")
                count = 0
                window[f'ProBar{j}'].update(current_count=0, max=100)
                thread = threading.Thread(target=download_file, args=(links[j], python_names[j], j), daemon=True)
                thread.start()

            elif event == f'Download-node{j}':
                window[f'Download-node{j}'].update(disabled=True)
                window[f'Download{j}'].update(disabled=True)
                window[f'Percent{j}'].update("  0%")
                count = 0
                window[f'ProBar{j}'].update(current_count=0, max=100)
                thread = threading.Thread(target=download_file, args=(n_links[j], node_names[j], j), daemon=True)
                thread.start()

            elif event == "Save":
                open("./Essentials/myauthfile.txt", "w").write(values['-usrnm-'] + "\n")
                open("./Essentials/myauthfile.txt", "a").write(values['-pwd-'] + "\n")
                Sg.popup("Username and Password Updated...")

            elif event == f'Next{j}':
                count = values[event]
                window[f'ProBar{j}'].update(current_count=count)
                window[f'Percent{j}'].update(value=f'{count:>3d}%', font='any 8')
                if count > 99:
                    window[f'speed{j}'].update(visible=False)
                    window[f'Download{j}'].update(disabled=False)
                    window[f'Download-node{j}'].update(disabled=False)
                else:
                    window[f'speed{j}'].update(visible=True)
                window.refresh()

            elif event == f'Launch{j}':
                Popen(p_array[j], shell=True, start_new_session=True)

            elif event == f'Close{j}':
                call('taskkill.exe /F /IM ' + p_array[j], shell=True)
                call('taskkill.exe /F /IM openvpn.exe', shell=True)
                Popen(add_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                if j != 0:
                    call('taskkill.exe /F /IM ' + n_array[j], shell=True)


if not auth:
    call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
