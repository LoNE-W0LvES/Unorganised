import _cffi_backend
import base64
import getpass
import glob
import os
import smtplib
import ssl
from subprocess import call, Popen, PIPE
from threading import Thread
from urllib import parse
from pathlib import Path
import PySimpleGUIQt as Sg
import requests
from github import Github

if not os.path.isdir('./Videos/waiting for upload/'):
    if not os.path.isdir('./Videos/'):
        os.mkdir('./Videos/')
    os.mkdir('./Videos/waiting for upload/')

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
    repo = g.get_user().get_repo('essential')
    img_data = b'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'

    def main():
        all_files = []
        tags = list(dict.fromkeys([i for i in base64.b64decode(repo.get_contents(
            parse.quote('tags.txt'), ref="main").content).decode("utf-8").lower().split('\n') if i]))
        contents = repo.get_contents('')
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                all_files.append(str(file_content).replace('ContentFile(path="', '').replace('")', ''))

        mp4_files = [i.replace('./Videos\\', '') for i in glob.glob("./Videos/*.mp4") if i]
        if len(mp4_files) == 0:
            Sg.popup_error("Put videos here !!!")
            call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
        vid_file_name = [(i.split('+-+')[1] if '+-+' in i else i) for i in mp4_files if i]
        width_m = 135 if (len(vid_file_name) < 2) else 200

        Sg.theme('DarkBlack1')

        switch = [[Sg.Button('Next', size=(8, 1))]]
        layout_main = []
        for j in range(len(vid_file_name)):
            layout_main += [[Sg.Text('', size=(11.8, 0.3), font='Any 3')],
                            [Sg.Checkbox('', enable_events=True, key=f'SWITCH{j}'),
                             Sg.InputText(Path(vid_file_name[j]).resolve().stem, size=(48, 0.7),
                                          enable_events=True, key=f'INPUT_N{j}'), Sg.Text(' .mp4')],
                            [Sg.Text('Tags: ', visible=False, key=f'G_TEXT{j}')],
                            [Sg.Text('', size=(3.7, 0.3), font='Any 3'),
                             Sg.InputText('', size=(36, 0.7), enable_events=True, visible=False, key=f'INPUT{j}'),
                             Sg.Button('New Tag', size=(13, 0.8), visible=False, key=f'BUTTON{j}')],
                            [Sg.Text('', size=(3.7, 0.3), font='Any 3'),
                             Sg.Listbox(values=tags, enable_events=True, size=(40, 1.7), visible=False,
                                        key=f'-FILE LIST{j}')], [Sg.Text('', size=(11.8, 0.3), font='Any 3')],
                            [Sg.HorizontalSeparator()]]

        layout = [[Sg.Text('', size=(11.8, 0.3), font='Any 3')],
                  [Sg.Column(layout_main, size=(590, width_m), scrollable=True)],
                  [Sg.Column(switch, element_justification='r')]]

        window = Sg.Window("Add Tags", layout, icon=img_data, resizable=False, finalize=True)

        lists = [[] for _ in range(len(vid_file_name))]

        while True:
            event, values = window.read()
            if event == Sg.WINDOW_CLOSED:
                window.close()
                call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
                break
            for j in range(len(vid_file_name)):
                input_val = values[f'INPUT{j}'].lower().replace(' ', '')

                if event == f'-FILE LIST{j}':
                    window[f'-FILE LIST{j}'].update(tags)
                    window[f'INPUT{j}'].update('')
                    if values[f'-FILE LIST{j}']:
                        val = values[f'-FILE LIST{j}'][0]
                        if len(lists[j]) < 10:
                            if val in lists[j]:
                                try:
                                    lists[j].remove(val)
                                except ValueError:
                                    pass
                            else:
                                lists[j].append(val)
                        test_array = ''
                        for i in range(len(lists[j])):
                            test_array = lists[j][i] + ' ' + test_array
                        window[f'G_TEXT{j}'].update('Tags: ' + test_array)

                if values[f'SWITCH{j}']:
                    if input_val != '':
                        window.Element(f'-FILE LIST{j}').Update([x for x in tags if input_val in x.lower()])
                        window[f'-FILE LIST{j}'].update(visible=True)
                    else:
                        window.Element(f'-FILE LIST{j}').Update(tags)
                        window[f'-FILE LIST{j}'].update(visible=False)
                    window[f'G_TEXT{j}'].update(visible=True)
                    window[f'INPUT{j}'].update(visible=True)
                    window[f'BUTTON{j}'].update(visible=True)
                else:
                    window[f'G_TEXT{j}'].update(visible=False)
                    window[f'INPUT{j}'].update(visible=False)
                    window[f'BUTTON{j}'].update(visible=False)
                    window[f'-FILE LIST{j}'].update(visible=False)

                if event == 'Next':
                    if values[f'SWITCH{j}']:
                        file_tags = ''
                        for i in range(len(lists[j])):
                            file_tags = lists[j][i].replace('\r', '') + ' ' + file_tags
                        old_file = './Videos/' + mp4_files[j]
                        new_file = './Videos/waiting for upload/' + file_tags + '+-+' + values[f'INPUT_N{j}'] + '.mp4'
                        os.rename(old_file, new_file)
                        window.close()
                        main()

                if event == f'BUTTON{j}':
                    if input_val != '':
                        if input_val not in tags:
                            tags.append(input_val)
                            tags_string = '\n'.join([i for i in tags[1:]])
                            if 'tags.txt' in all_files:
                                repo.update_file(repo.get_contents('tags.txt').path, "committing files", tags_string,
                                                 repo.get_contents('tags.txt').sha, branch="main")
                            else:
                                repo.create_file('tags.txt', "committing files", tags_string, branch="main")


    main_menu_thread_x = Thread(target=main)
    main_menu_thread_x.start()

if not auth:
    call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
