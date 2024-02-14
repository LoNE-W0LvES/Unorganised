import base64
import getpass
import glob
import os
import smtplib
import ssl
import subprocess
from threading import Thread
from urllib import parse

import PySimpleGUIQt as Sg
import requests
from github import Github

if not os.path.isdir('./Videos/'):
    os.mkdir('./Videos/')
if not os.path.isdir('./Videos/waiting for upload/'):
    os.mkdir('./Videos/waiting for upload/')
auth = False

hw_id = str(subprocess.Popen('wmic csproduct get uuid', shell=True,
                             stdout=subprocess.PIPE).communicate()[0]).split('\\r\\n')[1].strip('\\r').strip()

data_xxx = requests.get('https://pastebin.com/raw/kTWQnSx4').text

g = Github("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")
repo = g.get_user().get_repo('tags')

hwid = requests.get('https://pastebin.com/raw/y9e52zB6').text

if hw_id in hwid:
    auth = True
else:
    pc_username = getpass.getuser()
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "w3961500@gmail.com"
    receiver_email = "wolvesbatch1@gmail.com"
    password = 'wolvesbatch00'
    message = pc_username + '\n' + hw_id
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    Sg.popup("Wait for Verification")
    subprocess.call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)

if not os.path.isfile('./Essentials/app.ico'):
    open('./Essentials/app.ico', 'wb').write(base64.b64decode((g.get_user().get_repo('essential')).get_contents(
        parse.quote('icon.ico'), ref="main").content))

if auth:
    all_files = []
    contents = repo.get_contents('')
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))


    def main():

        games = ['']
        tags = ['']
        games.extend([i for i in base64.b64decode(repo.get_contents(parse.quote('games.txt'), ref="main").content
                                                  ).decode("utf-8").split('\n') if i])
        tags.extend([i for i in base64.b64decode(repo.get_contents(parse.quote('tags.txt'), ref="main").content
                                                 ).decode("utf-8").split('\n') if i])

        mp4_files = [i.replace('./Videos\\', '') for i in glob.glob("./Videos/*.mp4") if i]
        mp4_count = len(mp4_files)
        if mp4_count == 0:
            Sg.popup_error("Put videos here !!!")
            subprocess.call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)

        for file_name in mp4_files:
            new_name = ''
            game = ''
            tag_1 = ''
            tag_2 = ''
            tag_3 = ''
            tag_4 = ''
            tag_5 = ''
            tag_6 = ''
            tag_7 = ''
            tag_8 = ''
            tag_9 = ''

            substring = '+-+'

            if substring in file_name:
                new_f_name = file_name.split('+-+')[1]
            else:
                new_f_name = file_name

            switch = [[Sg.Button('Next', size=(8, 1))]]

            Add_new = [[Sg.Text('  Add New Game: ', size=(20, 0.7)), Sg.Text('  Add New Tag: ', size=(20, 0.7))],
                       [Sg.Input(do_not_clear=True, size=(20, 0.7), enable_events=True, key='_ADD-GAME_'),
                        Sg.Input(do_not_clear=True, size=(20, 0.7), enable_events=True, key='_ADD-TAG_')],
                       [Sg.Text('', size=(0.1, 0.7), font='Any 10'), Sg.Button('Add Game', size=(8, 1)),
                        Sg.Text('', size=(11.8, 0.7), font='Any 10'), Sg.Button('Add Tag', size=(8, 1))]]

            layout = [[Sg.Text('', font='Any 5')],
                      [Sg.Checkbox(new_f_name, enable_events=True, font='Any 15', key='SWITCH'),
                       Sg.Column(switch, element_justification='r')], [Sg.Text('', font='Any 5')],
                      [Sg.Input(do_not_clear=True, size=(20, 0.7), enable_events=True, key='_INPUT0_'),
                       Sg.Input(do_not_clear=True, size=(14, 0.7), enable_events=True, key='_INPUT1_'),
                       Sg.Input(do_not_clear=True, size=(14, 0.7), enable_events=True, key='_INPUT2_'),
                       Sg.Input(do_not_clear=True, size=(14, 0.7), enable_events=True, key='_INPUT3_'),
                       Sg.Input(do_not_clear=True, size=(14, 0.7), enable_events=True, key='_INPUT4_'),
                       Sg.Input(do_not_clear=True, size=(14, 0.7), enable_events=True, key='_INPUT5_'),
                       Sg.Input(do_not_clear=True, size=(14, 0.7), enable_events=True, key='_INPUT6_'),
                       Sg.Input(do_not_clear=True, size=(14, 0.7), enable_events=True, key='_INPUT7_'),
                       Sg.Input(do_not_clear=True, size=(14, 0.7), enable_events=True, key='_INPUT8_'),
                       Sg.Input(do_not_clear=True, size=(14, 0.7), enable_events=True, key='_INPUT9_')],
                      [Sg.Listbox(games, size=(20, 0.7), enable_events=True, key='_LIST0_'),
                       Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key='_LIST1_'),
                       Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key='_LIST2_'),
                       Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key='_LIST3_'),
                       Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key='_LIST4_'),
                       Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key='_LIST5_'),
                       Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key='_LIST6_'),
                       Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key='_LIST7_'),
                       Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key='_LIST8_'),
                       Sg.Listbox(tags, size=(14, 0.7), enable_events=True, key='_LIST9_')],
                      [Sg.Text(' G: ' + game, size=(20, 0.7), key='TEXT0'),
                       Sg.Text(' T1: ' + tag_1, size=(14, 0.7), key='TEXT1'),
                       Sg.Text(' T2: ' + tag_2, size=(14, 0.7), key='TEXT2'),
                       Sg.Text(' T3: ' + tag_3, size=(14, 0.7), key='TEXT3'),
                       Sg.Text(' T4: ' + tag_4, size=(14, 0.7), key='TEXT4'),
                       Sg.Text(' T5: ' + tag_5, size=(14, 0.7), key='TEXT5'),
                       Sg.Text(' T6: ' + tag_6, size=(14, 0.7), key='TEXT6'),
                       Sg.Text(' T7: ' + tag_7, size=(14, 0.7), key='TEXT7'),
                       Sg.Text(' T8: ' + tag_8, size=(14, 0.7), key='TEXT8'),
                       Sg.Text(' T9: ' + tag_9, size=(14, 0.7), key='TEXT9')],
                      [Sg.Column(Add_new, element_justification='l')], [Sg.Text('', font='Any 5')]]

            window = Sg.Window('Add tags!').Layout(layout)

            while True:
                event, values = window.Read()

                if event is None or event == 'Exit':
                    subprocess.call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
                ########################################################################################################
                if event == 'Add Game':
                    new_game = values['_ADD-GAME_'].lower()
                    if new_game not in tags:
                        games.append(new_game)
                        game_string = '\n'.join([i for i in games[1:]])
                        if 'game.txt' in all_files:
                            repo.update_file(repo.get_contents('game.txt').path, "committing files", game_string,
                                             repo.get_contents('game.txt').sha, branch="main")
                        else:
                            repo.create_file('game.txt', "committing files", game_string, branch="main")
                ########################################################################################################
                if event == 'Add Tag':
                    new_tag = values['_ADD-TAG_'].lower()
                    if new_tag not in tags:
                        tags.append(new_tag)
                        tags_string = '\n'.join([i for i in tags[1:]])
                        if 'tags.txt' in all_files:
                            repo.update_file(repo.get_contents('tags.txt').path, "committing files", tags_string,
                                             repo.get_contents('tags.txt').sha, branch="main")
                        else:
                            repo.create_file('tags.txt', "committing files", tags_string, branch="main")
                ########################################################################################################
                if values['_INPUT0_'] != '':
                    window.Element('_LIST0_').Update([x for x in games if values['_INPUT0_'].lower() in x])
                else:
                    window.Element('_LIST0_').Update(games)
                if event == '_LIST0_' and len(values['_LIST0_']):
                    game = values['_LIST0_'][0]
                    window.Element('TEXT0').Update(' G: ' + game)
                ########################################################################################################
                if values['_INPUT1_'] != '':
                    window.Element('_LIST1_').Update([x for x in games if values['_INPUT1_'].lower() in x])
                else:
                    window.Element('_LIST1_').Update(tags)
                if event == '_LIST1_' and len(values['_LIST1_']):
                    tag_1 = values['_LIST1_'][0]
                    window.Element('TEXT1').Update(' T1: ' + tag_1)
                ########################################################################################################
                if values['_INPUT2_'] != '':
                    window.Element('_LIST2_').Update([x for x in games if values['_INPUT2_'].lower() in x])
                else:
                    window.Element('_LIST2_').Update(tags)
                if event == '_LIST2_' and len(values['_LIST2_']):
                    tag_2 = values['_LIST2_'][0]
                    window.Element('TEXT2').Update(' T2: ' + tag_2)
                ########################################################################################################
                if values['_INPUT3_'] != '':
                    window.Element('_LIST3_').Update([x for x in games if values['_INPUT3_'].lower() in x])
                else:
                    window.Element('_LIST3_').Update(tags)
                if event == '_LIST3_' and len(values['_LIST3_']):
                    tag_3 = values['_LIST3_'][0]
                    window.Element('TEXT3').Update(' T3: ' + tag_3)
                ########################################################################################################
                if values['_INPUT4_'] != '':
                    window.Element('_LIST4_').Update([x for x in games if values['_INPUT4_'].lower() in x])
                else:
                    window.Element('_LIST4_').Update(tags)
                if event == '_LIST4_' and len(values['_LIST4_']):
                    tag_4 = values['_LIST4_'][0]
                    window.Element('TEXT4').Update(' T4: ' + tag_4)
                ########################################################################################################
                if values['_INPUT5_'] != '':
                    window.Element('_LIST5_').Update([x for x in games if values['_INPUT5_'].lower() in x])
                else:
                    window.Element('_LIST5_').Update(tags)
                if event == '_LIST5_' and len(values['_LIST5_']):
                    tag_5 = values['_LIST5_'][0]
                    window.Element('TEXT5').Update(' T5: ' + tag_5)
                ########################################################################################################
                if values['_INPUT6_'] != '':
                    window.Element('_LIST6_').Update([x for x in games if values['_INPUT6_'].lower() in x])
                else:
                    window.Element('_LIST6_').Update(tags)
                if event == '_LIST6_' and len(values['_LIST6_']):
                    tag_6 = values['_LIST6_'][0]
                    window.Element('TEXT6').Update(' T6: ' + tag_6)
                ########################################################################################################
                if values['_INPUT7_'] != '':
                    window.Element('_LIST7_').Update([x for x in games if values['_INPUT7_'].lower() in x])
                else:
                    window.Element('_LIST7_').Update(tags)
                if event == '_LIST7_' and len(values['_LIST7_']):
                    tag_7 = values['_LIST7_'][0]
                    window.Element('TEXT7').Update(' T7: ' + tag_7)
                ########################################################################################################
                if values['_INPUT8_'] != '':
                    window.Element('_LIST8_').Update([x for x in games if values['_INPUT8_'].lower() in x])
                else:
                    window.Element('_LIST8_').Update(tags)
                if event == '_LIST8_' and len(values['_LIST8_']):
                    tag_8 = values['_LIST8_'][0]
                    window.Element('TEXT8').Update(' T8: ' + tag_8)
                ########################################################################################################
                if values['_INPUT9_'] != '':
                    window.Element('_LIST9_').Update([x for x in games if values['_INPUT9_'].lower() in x])
                else:
                    window.Element('_LIST9_').Update(tags)
                if event == '_LIST9_' and len(values['_LIST9_']):
                    tag_9 = values['_LIST9_'][0]
                    window.Element('TEXT9').Update(' T9: ' + tag_9)
                ########################################################################################################
                if event == 'Next':
                    if game != '':
                        raw_tags = game
                        if tag_1 != '' and tag_1 != tag_2 and tag_1 != tag_3 and tag_1 != tag_4 and tag_1 != tag_5 and \
                                tag_1 != tag_6 and tag_1 != tag_7 and tag_1 != tag_8 and tag_1 != tag_9:
                            raw_tags = raw_tags + ' ' + tag_1
                        if tag_2 != '' and tag_2 != tag_1 and tag_2 != tag_3 and tag_2 != tag_4 and tag_2 != tag_5 and \
                                tag_2 != tag_6 and tag_2 != tag_7 and tag_2 != tag_8 and tag_2 != tag_9:
                            raw_tags = raw_tags + ' ' + tag_2
                        if tag_3 != '' and tag_3 != tag_2 and tag_3 != tag_1 and tag_3 != tag_4 and tag_3 != tag_5 and \
                                tag_3 != tag_6 and tag_3 != tag_7 and tag_3 != tag_8 and tag_3 != tag_9:
                            raw_tags = raw_tags + ' ' + tag_3
                        if tag_4 != '' and tag_4 != tag_2 and tag_4 != tag_3 and tag_4 != tag_1 and tag_4 != tag_5 and \
                                tag_4 != tag_6 and tag_4 != tag_7 and tag_4 != tag_8 and tag_4 != tag_9:
                            raw_tags = raw_tags + ' ' + tag_4
                        if tag_5 != '' and tag_5 != tag_2 and tag_5 != tag_3 and tag_5 != tag_4 and tag_5 != tag_1 and \
                                tag_5 != tag_6 and tag_5 != tag_7 and tag_5 != tag_8 and tag_5 != tag_9:
                            raw_tags = raw_tags + ' ' + tag_5
                        if tag_6 != '' and tag_6 != tag_2 and tag_6 != tag_3 and tag_6 != tag_4 and tag_6 != tag_5 and \
                                tag_1 != tag_6 and tag_6 != tag_7 and tag_6 != tag_8 and tag_6 != tag_9:
                            raw_tags = raw_tags + ' ' + tag_6
                        if tag_7 != '' and tag_7 != tag_2 and tag_7 != tag_3 and tag_7 != tag_4 and tag_7 != tag_5 and \
                                tag_7 != tag_6 and tag_1 != tag_7 and tag_7 != tag_8 and tag_7 != tag_9:
                            raw_tags = raw_tags + ' ' + tag_7
                        if tag_8 != '' and tag_8 != tag_2 and tag_8 != tag_3 and tag_8 != tag_4 and tag_8 != tag_5 and \
                                tag_8 != tag_6 and tag_8 != tag_7 and tag_8 != tag_1 and tag_8 != tag_9:
                            raw_tags = raw_tags + ' ' + tag_8
                        if tag_9 != '' and tag_9 != tag_2 and tag_9 != tag_3 and tag_9 != tag_4 and tag_9 != tag_5 and \
                                tag_9 != tag_6 and tag_9 != tag_7 and tag_9 != tag_8 and tag_9 != tag_1:
                            raw_tags = raw_tags + ' ' + tag_9

                        if file_name != '':
                            new_name = raw_tags + '+-+' + new_f_name

                        old_file = './Videos/' + file_name
                        new_file = './Videos/waiting for upload/' + new_name
                        if values['SWITCH']:
                            os.rename(old_file, new_file)
                        window.close()
                        break
                    else:
                        if values['SWITCH']:
                            Sg.popup('Add Tags')
                        else:
                            window.close()
                            break


    main_menu_thread_x = Thread(target=main)
    main_menu_thread_x.start()

if not auth:
    subprocess.call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
