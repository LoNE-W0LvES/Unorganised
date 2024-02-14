# import glob
# import hashlib
# import sys
#
# import requests
# import threading
# from time import sleep
# from random import randint
# import PySimpleGUIQt as sg
# from math import floor
#
# from tqdm import tqdm
# from github import Github
#
#
# g = Github("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")
# header = {"Authorization": "token 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",
#           "Accept": "application/vnd.github.v4.raw"}
# link_up = 'https://raw.githubusercontent.com/WoLvES-2x0/python-files/main/upload ec3759522b53fa2c4418d87e21342c22'
# g_f_name = [str(i).replace('ContentFile(path="', '').replace('")', '') for i in
#             (g.get_user().get_repo('python-files')).get_contents('') if i]
# link_head = 'https://raw.githubusercontent.com/WoLvES-2x0/python-files/main/'
#
# python_hash = ' '.join(map(str, g_f_name)).lower().split(' ')
#
# files_hash = ','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in [
#     i for i in glob.glob("*.exe") if i]])).lower().split(',')
#
# # def download(url: str, fname: str):
# #     resp = requests.get(url, headers=header, stream=True)
# #     total = int(resp.headers.get('content-length', 0))
# #     with open(fname, 'wb') as file, tqdm(
# #         desc=fname,
# #         total=total,
# #         unit='iB',
# #         unit_scale=True,
# #         unit_divisor=1024,
# #     ) as bar:
# #         for data in resp.iter_content(chunk_size=1024):
# #             size = file.write(data)
# #             bar.update(size)
#
# # download(link_head, o_path)
#
#
# def download_file(windows, link, f_name):
#     resp = requests.get(link, headers=header, stream=True)
#     total = int(resp.headers.get('content-length', 0))
#     ceil_value = floor(total / 100)
#     with open(f_name, 'wb') as file, tqdm(desc=f_name, total=total, unit='iB', unit_scale=True, unit_divisor=ceil_value,
#     ) as bar:
#         x_i = 0
#         for data in resp.iter_content(chunk_size=ceil_value):
#             size = file.write(data)
#             bar.update(size)
#             windows.write_event_value('Next', x_i)
#             x_i = x_i + 1
#
#
# print('k')
#
#
# sg.theme("DarkBlue")
#
# progress_bar = [
#     [sg.ProgressBar(100, size=(40, 20), pad=(0, 0), key='Progress Bar'),
#      sg.Text("  0%", size=(4, 1), key='Percent')],
# ]
#
# layout = [
#     [sg.Button('Download')],
#     [sg.Column(progress_bar, key='Progress')],
# ]
# window = sg.Window('Title', layout, size=(520, 80), finalize=True, use_default_focus=False)

# try:
#     upload_hash = python_hash[python_hash.index('upload') + 1]
#     upload_file_name = files_hash[files_hash.index(upload_hash) - 1]
#     print('Found: ' + upload_file_name)
# except ValueError:
#     print('File not found')
#     link_upload = link_head + [i.lower() for i in g_f_name if 'upload' in i][0]
#
# file_name = 'upload-launcher.exe'
# #     count = 0
# #     window['Progress Bar'].update(current_count=0, max=100)
# thread = threading.Thread(target=download_file, args=(window, link_up, file_name), daemon=True)
# thread.start()
# print('Download Finished')
#
# while True:
#     event, values = window.read()
#     if event == sg.WINDOW_CLOSED:
#         break
#
#     if event == 'Download':
#         count = 0
#         window['Progress Bar'].update(current_count=0, max=100)
#         thread = threading.Thread(target=download_file, args=(window, ), daemon=True)
#         thread.start()
#     elif event == 'Next':
#         count = values[event]
#         window['Progress Bar'].update(current_count=count)
#         window['Percent'].update(value=f'{count:>3d}%')
#         window.refresh()

        # if upload_n_hash not in files_hash:
        #     window['Launch1'].update(disabled=True)
        # else:
        #     upload_n_name = files_hash[files_hash.index(upload_n_hash) - 1]
        #     if upload_name not in (i.name() for i in psutil.process_iter()):
        #         window['Launch1'].update(disabled=False)
        #         window['Close1'].update(disabled=True)
        #     else:
        #         window['Launch1'].update(disabled=True)
        #         window['Close1'].update(disabled=False)

        # if create_n_hash not in files_hash:
        #     window['Launch2'].update(disabled=True)
        # else:
        #     create_n_name = files_hash[files_hash.index(create_n_hash) - 1]
        #     if create_name not in (i.name() for i in psutil.process_iter()):
        #         window['Launch2'].update(disabled=False)
        #         window['Close2'].update(disabled=True)
        #     else:
        #         window['Launch2'].update(disabled=True)
        #         window['Close2'].update(disabled=False)

        # if view_n_hash not in files_hash:
        #     window['Launch3'].update(disabled=True)
        # else:
        #     view_n_name = files_hash[files_hash.index(view_n_hash) - 1]
        #     if view_name not in (i.name() for i in psutil.process_iter()):
        #         window['Launch3'].update(disabled=False)
        #         window['Close3'].update(disabled=True)
        #     else:
        #         window['Launch3'].update(disabled=True)
        #         window['Close3'].update(disabled=False)



# import base64
#
# import subprocess
# import PySimpleGUIQt as Sg
# import requests
# header = {"Authorization": "token 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",
#           "Accept": "application/vnd.github.v4.raw"}
# encoded = base64.b64encode((requests.get('https://raw.githubusercontent.com/WoLvES-2x0/python-files/main/create.ico', headers=header)).content)
#
#
# hw_id = str(subprocess.Popen('wmic csproduct get uuid', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]).split('\\r\\n')[1].strip('\\r').strip()
#
# layout = [
#     [Sg.Text(hw_id)]
# ]
# window = Sg.Window("Add Tags", layout, icon=encoded, resizable=False, finalize=True)
# while True:
#     event, values = window.read()
#     if event == Sg.WINDOW_CLOSED:
#         window.close()
#         break
#
# # start_new_session=True

# files_hash = ['hi', 'bye', 'sakura', 'moon', 'upload_hash', 'upload_n_hash']
#
#
# if 'upload_hash' and 'upload_n_hash' not in files_hash:
#     print('gg')
#
# import _cffi_backend
# import glob
# import hashlib
# from subprocess import call, Popen, PIPE
# from time import monotonic
#
# import psutil
# import requests
# import threading
#
# import PySimpleGUI as Sg
# from github import Github
#
# from math import floor
#
# g = Github("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")
# header = {"Authorization": "token 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",
#           "Accept": "application/vnd.github.v4.raw"}
#
# g_p_f_name = [str(i).replace('ContentFile(path="', '').replace('")', '') for i in
#               (g.get_user().get_repo('python-files')).get_contents('') if i]
# git_p_hf = ' '.join(map(str, g_p_f_name)).lower().split(' ')
# link_head = 'https://raw.githubusercontent.com/WoLvES-2x0/python-files/main/'
# link_tag = "{0}{1}".format(link_head, [i for i in g_p_f_name if 'addtags' in i.lower()][0])
# link_upload = "{0}{1}".format(link_head, [i for i in g_p_f_name if 'upload' in i.lower()][0])
# link_create = "{0}{1}".format(link_head, [i for i in g_p_f_name if 'create' in i.lower()][0])
# link_view = "{0}{1}".format(link_head, [i for i in g_p_f_name if 'view' in i.lower()][0])
#
#
# g_n_f_name = [str(i).replace('ContentFile(path="', '').replace('")', '') for i in
#               (g.get_user().get_repo('node-files')).get_contents('') if i]
# git_n_hf = ' '.join(map(str, g_n_f_name)).lower().split(' ')
# link_n_head = 'https://raw.githubusercontent.com/WoLvES-2x0/node-files/main/'
# link_n_tag = ''
# link_n_upload = "{0}{1}".format(link_n_head, [i for i in g_n_f_name if 'upload' in i.lower()][0])
# link_n_create = "{0}{1}".format(link_n_head, [i for i in g_n_f_name if 'create' in i.lower()][0])
# link_n_view = "{0}{1}".format(link_n_head, [i for i in g_n_f_name if 'view' in i.lower()][0])
#
# links = [link_tag, link_upload, link_create, link_view]
# n_links = [link_n_tag, link_n_upload, link_n_create, link_n_view]
# python_names = ['tags-part1.exe', 'upload-part1.exe', 'create-part1.exe', 'view-part1.exe']
# node_names = ['tags-part2.exe', 'upload-part2.exe', 'create-part2.exe', 'view-part2.exe']
# just_name = ['Tag', 'Upload', 'Create', 'View']
# tags_name = ''
# upload_name = ''
# create_name = ''
# view_name = ''
# upload_n_name = ''
# create_n_name = ''
# view_n_name = ''
# p_array = []
#
#
# def download_file(link, f_name, k):
#     r = requests.get(link, headers=header, stream=True)
#     file_size = int(r.headers['content-length'])
#     ceil_value = floor(file_size / 100)
#     downloaded = 0
#     start = monotonic()
#     with open(f_name, 'wb') as fp:
#         for chunk in r.iter_content(chunk_size=ceil_value):
#             downloaded += fp.write(chunk)
#             now = monotonic()
#             c_out = round(downloaded / file_size * 100)
#
#             window.write_event_value(f'Next{k}', c_out)
#             window[f'speed{k}'].update('S: ' + f'{round(downloaded / (now - start) / 1024) / 1024:.2f}' +
#                                        " MBps  D: " + f'{round(downloaded / 1024) / 1024:.2f}' + " MB",
#                                        font='any 8')
#
#
# def test_thread():
#     global tags_name
#     global upload_name
#     global create_name
#     global view_name
#     global p_array
#     global upload_n_name
#     global create_n_name
#     global view_n_name
#     while True:
#         files_hash = ','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in
#                                         [i for i in glob.glob("*.exe") if i]])).split(',')
#         tags_hash = git_p_hf[git_p_hf.index('addtags') + 1]
#         upload_hash = git_p_hf[git_p_hf.index('upload') + 1]
#         create_hash = git_p_hf[git_p_hf.index('create') + 1]
#         view_hash = git_p_hf[git_p_hf.index('view') + 1]
#         upload_n_hash = git_n_hf[git_n_hf.index('upload') + 1]
#         create_n_hash = git_n_hf[git_n_hf.index('create') + 1]
#         view_n_hash = git_n_hf[git_n_hf.index('view') + 1]
#         window['Launch3'].update(disabled=True)
#
#         if tags_hash in files_hash:
#             tags_name = files_hash[files_hash.index(tags_hash) - 1]
#             if tags_name not in (i.name() for i in psutil.process_iter()):
#                 window['Launch0'].update(disabled=False)
#                 window['Close0'].update(disabled=True)
#             else:
#                 window['Launch0'].update(disabled=True)
#                 window['Close0'].update(disabled=False)
#         else:
#             window['Download-node0'].update(disabled=True)
#             tags_name = ''
#
#         if upload_hash in files_hash and upload_n_hash in files_hash:
#             upload_name = files_hash[files_hash.index(upload_hash) - 1]
#             if upload_name not in (i.name() for i in psutil.process_iter()):
#                 window['Launch1'].update(disabled=False)
#                 window['Close1'].update(disabled=True)
#             else:
#                 window['Launch1'].update(disabled=True)
#                 window['Close1'].update(disabled=False)
#                 print('o')
#         else:
#             window['Launch1'].update(disabled=True)
#             upload_name = ''
#
#         if create_hash in files_hash and create_n_hash in files_hash:
#             create_name = files_hash[files_hash.index(create_hash) - 1]
#             if create_name not in (i.name() for i in psutil.process_iter()):
#                 window['Launch2'].update(disabled=False)
#                 window['Close2'].update(disabled=True)
#             else:
#                 window['Launch2'].update(disabled=True)
#                 window['Close2'].update(disabled=False)
#         else:
#             window['Launch2'].update(disabled=True)
#             create_name = ''
#
#         if view_hash in files_hash and view_n_hash in files_hash:
#             view_name = files_hash[files_hash.index(view_hash) - 1]
#             if view_name not in (i.name() for i in psutil.process_iter()):
#                 window['Launch3'].update(disabled=False)
#                 window['Close3'].update(disabled=True)
#             else:
#                 window['Launch3'].update(disabled=True)
#                 window['Close3'].update(disabled=False)
#         else:
#             window['Launch3'].update(disabled=True)
#             view_name = ''
#
#         p_array = [tags_name, upload_name, create_name, view_name]
#
#
# thread_x = threading.Thread(target=test_thread)
# thread_x.start()
#
# Sg.theme("DarkBlue")
# layout = []
# for j in range(len(links)):
#     layout += [[Sg.Text(just_name[j], font='any 15')],
#                [Sg.Button('Download PART1', size=(15, 1), key=f'Download{j}'), Sg.Button('Download PART2', size=(15, 1), key=f'Download-node{j}'),
#                 Sg.Text("              "), Sg.Button('Launch \'' + just_name[j] + '\'', size=(15, 1), key=f'Launch{j}'),
#                 Sg.Button('Close \'' + just_name[j] + '\'', size=(15, 1), disabled=True, key=f'Close{j}')],
#                [Sg.ProgressBar(100, size=(40, 1), pad=(0, 0), key=f'ProBar{j}'),
#                 Sg.Text("  0%", size=(4, 1), font='any 8', key=f'Percent{j}'), Sg.Text("", visible=False, font='any 8', key=f'speed{j}')]]
#
# window = Sg.Window('Title', layout, finalize=True, use_default_focus=False)
#
# while True:
#
#     event, values = window.read()
#     if event == Sg.WINDOW_CLOSED:
#         break
#     for j in range(len(links)):
#         if event == f'Download{j}':
#             window[f'Download{j}'].update(disabled=True)
#             window[f'Download-node{j}'].update(disabled=True)
#             window[f'Percent{j}'].update("  0%")
#             count = 0
#             window[f'ProBar{j}'].update(current_count=0, max=100)
#             thread = threading.Thread(target=download_file, args=(links[j], python_names[j], j), daemon=True)
#             thread.start()
#
#         if event == f'Download-node{j}':
#             window[f'Download-node{j}'].update(disabled=True)
#             window[f'Download{j}'].update(disabled=True)
#             window[f'Percent{j}'].update("  0%")
#             count = 0
#             window[f'ProBar{j}'].update(current_count=0, max=100)
#             thread = threading.Thread(target=download_file, args=(n_links[j], node_names[j], j), daemon=True)
#             thread.start()
#
#         elif event == f'Next{j}':
#             count = values[event]
#             window[f'ProBar{j}'].update(current_count=count)
#             window[f'Percent{j}'].update(value=f'{count:>3d}%', font='any 8')
#             if count > 99:
#                 window[f'speed{j}'].update(visible=False)
#                 window[f'Download{j}'].update(disabled=False)
#                 window[f'Download-node{j}'].update(disabled=False)
#             else:
#                 window[f'speed{j}'].update(visible=True)
#             window.refresh()
#
#         elif event == f'Launch{j}':
#             Popen(p_array[j], start_new_session=True)
#
#         elif event == f'Close{j}':
#             call('taskkill.exe /F /IM ' + p_array[j], shell=True)
# import sys
#
# print('Argument List:', str(sys.argv))


#!/usr/bin/env python
import base64
import string
import sys

# import PySimpleGUIQt as sg
#
# tab1_layout = [[sg.T('Tab 1')],
#                [sg.T('Put your layout in here')],
#                [sg.T('Input something'),sg.In(key='_in0_')]]
#
# tab2_layout = [[sg.T('Tab2')]]
#
#
# layout = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout, key='_tab1_'), sg.Tab('Tab 2', tab2_layout, key='_tab2_')]])],
#                          [sg.RButton('Disable 1'), sg.RButton('Disable 2'), sg.RButton('Enable 1'), sg.RButton('Enable 2')]]
#
# window = sg.Window('My window with tabs', default_element_size=(12,1)).Layout(layout)
#
#
# while True:
#     b, v = window.Read()
#     # sg.PopupNonBlocking('button = %s'%b,'Values dictionary', v)
#     print(b, v)
#     if b is None:           # always,  always give a way out!
#         break
#     if b == 'Disable 1':
#         window.FindElement('_tab1_').Update(disabled=True)
#     elif b == 'Enable 1':
#         window.FindElement('_tab1_').Update(disabled=False)
#     elif b == 'Disable 2':
#         window.FindElement('_tab2_').Update(disabled=True)
#     elif b == 'Enable 2':
#         window.FindElement('_tab2_').Update(disabled=False)
# from urllib import parse
import random
# from github import Github
#
# g = Github("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")
# tk = [i for i in base64.b64decode((g.get_user().get_repo('essential')).get_contents(
#     parse.quote('tkifinfo.txt'), ref="main").content).decode("utf-8").replace('\r', '').split('\n') if i]
#
# token = random.choice(tk)
# print(token)

# tt = (''.join(random.SystemRandom().choice(string.digits) for _ in range(random.(8))))

import random

my_list = list(range(0, 8))
random.shuffle(my_list)
print(my_list)
