import json
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
import base64
import _cffi_backend
import os
import base64
import subprocess
import firebase_admin
import PySimpleGUI as Sg
from firebase_admin import db
from firebase_admin import credentials
from threading import Thread
import PySimpleGUI as Sg
import psutil
import requests
from github import Github
import time
from math import floor
from stuff import stuff
from customer import customer


def write_json(filename, json_data):
    if os.path.exists(filename) and open(filename).read() is not None:
        with open(filename) as fx:
            obj = json.load(fx)
        obj.append(json_data)
    else:
        obj = json_data
    with open(filename, "w+") as of:
        json.dump(obj, of)


stuff_ids = open('./Stuff/stuffID.txt', 'r').read().split('\n')

found_stuff = 0
links = ['sdas', 'afdsf', 'asddgf', 'dffhfg']
select_user = False
select_user_login = False
Sg.theme("DarkBlue")
stuff_loc = './Stuff/stuff.json'
customer_loc = './Customer/customer.json'
file_pass = [[Sg.FileBrowse(file_types=(("jpg File", "*.jpg"), ("png File", "*.png")), key='file-passport')]]
file_sig = [[Sg.FileBrowse(file_types=(("jpg File", "*.jpg"), ("png File", "*.png")), key='file-signature')]]
file_nid = [[Sg.FileBrowse(file_types=(("jpg File", "*.jpg"), ("png File", "*.png")), key='file-nid')]]
signin_layout = [[Sg.Text("                             Log In                             ", font='Any 25')],
                 [Sg.DropDown(['Customer', 'Stuff'], default_value='Customer', key='-select-user-login-'), Sg.Button("Select User", size=(10, 1), key='-s-u-login-')],
                 [Sg.Text("Phone", size=(10, 1), font='Any 13', key='user-login', enable_events=True), Sg.InputText(key='-usrnm-login-', font='Any 10')],
                 [Sg.Text("Password", size=(10, 1), font='Any 13'), Sg.InputText(key='-pwd-', password_char='*', font='Any 10')],
                 [Sg.Text(" ")],
                 [Sg.Button("Login", size=(10, 1), visible=True)]]

signup_layout = [[Sg.Text("                            Register                            ", font='Any 25')],
                 [Sg.Text(" ")],
                 [Sg.Text("User ", size=(13, 1), font='Any 10'),
                  Sg.DropDown(['Customer', 'Stuff'], default_value='Customer', key='-select-user-'), Sg.Button("Select User", size=(10, 1))],
                 [Sg.Text("First Name", size=(13, 1), font='Any 10'),
                 Sg.InputText(key='-usrnm-f-', font='Any 10')],
                 [Sg.Text("Last Name", size=(13, 1), font='Any 10'),
                 Sg.InputText(key='-usrnm-l-', font='Any 10')],
                 [Sg.Text("Email", size=(13, 1), font='Any 10'),
                  Sg.InputText(key='-mail-', font='Any 10')],
                 [Sg.Text("Phone", size=(13, 1), font='Any 10'),
                  Sg.InputText(key='-phone-', font='Any 10')],
                 [Sg.Text("Gender", size=(13, 1), font='Any 10'),
                  Sg.DropDown(['Male', 'Female'], default_value='Male', key='-select-gender-')],
                 [Sg.Text("Address", size=(13, 1), font='Any 10'),
                  Sg.InputText(key='-address-', font='Any 10')],
                 [Sg.Text("Hair color", size=(13, 1), font='Any 10', key='-hc-t-'),
                  Sg.InputText(key='-hc-', font='Any 10', disabled=False)],
                 [Sg.Text("Eye color", size=(13, 1), font='Any 10', key='-ec-t-'),
                  Sg.InputText(key='-ec-', font='Any 10', disabled=False)],
                 [Sg.Text("Height", size=(13, 1), font='Any 10', key='-h-t-'),
                  Sg.InputText(key='-height-', font='Any 10', disabled=False)],
                 [Sg.Text("Weight", size=(13, 1), font='Any 10', key='-w-t-'),
                  Sg.InputText(key='-weight-', font='Any 10', disabled=False)],
                 [Sg.Text("Stuff ID", size=(13, 1), font='Any 10', key='-st-t-'),
                  Sg.InputText(key='-st-', font='Any 10', disabled=True)],
                 [Sg.Text("Password", size=(13, 1), font='Any 10'),
                 Sg.InputText(key='-pwd-1-', password_char='*', font='Any 10')],
                 [Sg.Text("Confirm Password", size=(13, 1), font='Any 10'),
                 Sg.InputText(key='-pwd-2-', password_char='*', font='Any 10')],
                 [Sg.Text(" ")],
                 [Sg.Text("Upload a passport size photo: ", size=(22, 1)), Sg.Column(file_pass)],
                 [Sg.Text("Upload signature: ", size=(22, 1)), Sg.Column(file_sig)],
                 [Sg.Text("Upload NID: ", size=(22, 1)), Sg.Column(file_nid)],
                 [Sg.Checkbox("I agree to Terms", size=(13, 1), font='Any 10')],
                 [Sg.Text(" ")],
                 [Sg.Button("Register", size=(10, 1), visible=True)]]

tab_g_l = [[Sg.Tab('                              Sign in                               ',
                   signin_layout, font='Courier 15', key='-TAB1-'),
            Sg.Tab('                              Sign up                               ',
                   signup_layout, visible=True, key='-TAB2-')]]

layout = [[Sg.TabGroup(tab_g_l, title_color='#0f0f0f', enable_events=True, key='-TAB0-')],
          [Sg.Text("", size=(20, 1), font='Any 8', key='status')]]

window = Sg.Window('Launcher', layout, use_default_focus=False, resizable=False, finalize=True)
# thread_x = threading.Thread(target=test_thread)
# thread_x.start()

while True:
    event, values = window.read()
    print(event)
    if event == Sg.WINDOW_CLOSED:
        call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
        break
    elif event == "Select User":
        select_user = False if values['-select-user-'] == 'Customer' else True

        window['-st-'].update(disabled=not select_user)
    elif event == "-s-u-login-":
        if values['-select-user-login-'] == 'Stuff':
            window['user-login'].update('Stuff ID')
        else:
            window['user-login'].update('Phone')

    elif event == "Login":
        if values['-select-user-login-'] == 'Stuff':
            f = open(stuff_loc)
            data = json.load(f)
            d2 = {}
            for i in data:
                if i['User type'] == 'Stuff':
                    if i['id'] == values['-usrnm-login-']:
                        if i['password'] == values['-pwd-']:
                            d2 = i
                            Sg.popup('Logged in')
                            window.close()
                            stuff()
                        else:
                            Sg.popup('User/Password Error')
                        break

            if d2 == {}:
                Sg.popup('User/Password Error')
        else:
            f = open(stuff_loc)
            data = json.load(f)
            d1 = {}
            for i in data:
                if i['User type'] == 'Customer':
                    if i['phone'] == values['-usrnm-login-']:
                        d1 = i
                        print(d1)
                        break
            if d1 == {}:
                Sg.popup('User/Password Error')
            else:
                if d1['password'] == values['-pwd-']:
                    Sg.popup('Logged in')
                    window.close()
                    customer(d1)
                else:
                    print("err")
                    Sg.popup('User/Password Error')

    elif event == "Register":
        if values['-select-user-'] == 'Stuff':
            st_id = True if values['-st-'] in stuff_ids else False

            if values['-st-'] == '':
                Sg.popup('Stuff ID Required.')
            if not st_id:
                Sg.popup('Not an stuff.')
            else:
                if values['-pwd-1-'] != values['-pwd-2-']:
                    Sg.popup('Check Password.')
                else:
                    data = {
                        "User type": values['-select-user-'],
                        "id": values['-st-'],
                        "Name": values['-usrnm-f-'] + values['-usrnm-l-'],
                        "phone": values['-phone-'],
                        "Email": values['-mail-'],
                        "password": values['-pwd-1-'],
                        "Gender": values['-select-gender-'],
                        "Hair color": values['-hc-'],
                        "Eye color": values['-ec-'],
                        "Height": values['-height-'],
                        "Weight": values['-weight-'],
                        "address": values['-address-'],
                        "Borrowed Date": '',
                        "Box Size": '',
                        "Box Price": '',
                        "Time Limit": ''
                    }
                    write_json(stuff_loc, data)
                    Sg.popup('Login.')
        elif values['-select-user-'] == 'Customer':
            if values['-phone-'] == '':
                Sg.popup('Phone number Required.')
            else:
                if values['-pwd-1-'] != values['-pwd-2-']:
                    Sg.popup('Check Password.')
                else:
                    data = {
                        "User type": values['-select-user-'],
                        "id": values['-phone-'],
                        "Name": values['-usrnm-f-'] + values['-usrnm-l-'],
                        "phone": values['-phone-'],
                        "Email": values['-mail-'],
                        "password": values['-pwd-1-'],
                        "Gender": values['-select-gender-'],
                        "Hair color": values['-hc-'],
                        "Eye color": values['-ec-'],
                        "Height": values['-height-'],
                        "Weight": values['-weight-'],
                        "address": values['-address-'],
                        "Borrowed Date": '',
                        "Box Size": '',
                        "Box Price": '',
                        "Time Limit": ''
                    }
                    write_json(stuff_loc, data)
                    Sg.popup('Login.')

window.close()



        # print(event)
    # for j in range(len(links)):
    #     if event == f'Download{j}':
    #         window[f'Download{j}'].update(disabled=True)
    #         window[f'Download-node{j}'].update(disabled=True)
    #         window[f'Percent{j}'].update("  0%")
    #         count = 0
    #         window[f'ProBar{j}'].update(current_count=0, max=100)
    #         # thread = threading.Thread(target=download_file, args=(links[j], python_names[j], j), daemon=True)
    #         # thread.start()
    #
    #     elif event == f'Download-node{j}':
    #         window[f'Download-node{j}'].update(disabled=True)
    #         window[f'Download{j}'].update(disabled=True)
    #         window[f'Percent{j}'].update("  0%")
    #         count = 0
    #         window[f'ProBar{j}'].update(current_count=0, max=100)
    #         # thread = threading.Thread(target=download_file, args=(n_links[j], node_names[j], j), daemon=True)
    #         # thread.start()
    #
    #     elif event == "Save":
    #         open("./Essentials/myauthfile.txt", "w").write(values['-usrnm-'] + "\n")
    #         open("./Essentials/myauthfile.txt", "a").write(values['-pwd-'] + "\n")
    #         Sg.popup("Username and Password Updated...")
    #
    #     elif event == f'Next{j}':
    #         count = values[event]
    #         window[f'ProBar{j}'].update(current_count=count)
    #         window[f'Percent{j}'].update(value=f'{count:>3d}%', font='any 8')
    #         if count > 99:
    #             window[f'speed{j}'].update(visible=False)
    #             window[f'Download{j}'].update(disabled=False)
    #             window[f'Download-node{j}'].update(disabled=False)
    #         else:
    #             window[f'speed{j}'].update(visible=True)
    #         window.refresh()
    #
    #     elif event == f'Launch{j}':
    #         Popen(p_array[j], shell=True, start_new_session=True)
    #
    #     elif event == f'Close{j}':
    #         call('taskkill.exe /F /IM ' + p_array[j], shell=True)
    #         call('taskkill.exe /F /IM openvpn.exe', shell=True)
    #         Popen(add_route, shell=True, start_new_session=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    #         if j != 0:
    #             call('taskkill.exe /F /IM ' + n_array[j], shell=True)




