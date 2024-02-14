import getpass
import math
import os
import re
import sys
import time
from pathlib import Path
from subprocess import Popen, PIPE, call

import PySimpleGUIQt as Sg
import psutil
from win32com.client import Dispatch

from threading import Thread

f_n_hp = 'processHP.txt'
f_n_b = 'processB.txt'
user_name = getpass.getuser()
new_name = Path(os.path.basename(sys.argv[0])).resolve().stem
if not os.path.isfile(f_n_b):
    open(f_n_b, "w+")
if not os.path.isfile(f_n_hp):
    open(f_n_hp, "w+")
if not os.path.isfile('scheme.txt') or len(open('scheme.txt', 'r').readlines()) < 3:
    open('scheme.txt', "w+").write('\n\n\n')
path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\%s.lnk' % (user_name, new_name)
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = r"%s\%s" % (os.getcwd(), os.path.basename(sys.argv[0]))
shortcut.WorkingDirectory = os.getcwd()
shortcut.save()


cfg = open('scheme.txt', 'r').readlines()
default = cfg[0].replace('\n', '')
first = cfg[1].replace('\n', '')
second = cfg[2].replace('\n', '')
ax = ''
bx = ''
cx = ''


def multiple_replace(string, rep_dict):
    pat = re.compile("|".join([re.escape(str(k)) for k in sorted(rep_dict, key=len, reverse=True)]), flags=re.DOTALL)
    return pat.sub(lambda x: rep_dict[x.group(0)], string)


s_call = Popen('powercfg /list', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()[0].decode("utf-8")
replacing = multiple_replace(s_call, {'Power Scheme GUID:': 'powercfg /setactive', ')': '', ' *': '', '  (': '+'})
all_scheme = '+'.join(replacing.split('\r\n')[3:-1]).split('+')
for_default = for_first = for_second = [all_scheme[(i*2)+1] for i in range(math.floor(len(all_scheme)/2))]


def main():
    switch = True
    while True:
        global ax
        global bx
        global cx
        pro_b = []
        pro_hp = []
        p_a_b = []
        p_a_hp = []
        default_x = ''
        secondary = ''
        game = ''
        time.sleep(1)
        pro_hp.clear()
        pro_b.clear()
        clean0 = "".join(line for line in open(f_n_hp) if not line.isspace())
        clean1 = "".join(line for line in open(f_n_b) if not line.isspace())
        open(f_n_hp, 'w+').write(clean0)
        open(f_n_b, 'w+').write(clean1)
        p_a_hp.clear()
        p_a_b.clear()
        for hpa in open(f_n_hp).readlines():
            p_a_hp.append(hpa.replace("\n", ""))
        for tk in open(f_n_b).readlines():
            p_a_b.append(tk.replace("\n", ""))

        cfg_x = open('scheme.txt', 'r').readlines()

        for i in range(len(all_scheme)):
            if all_scheme[i] == cfg_x[0].replace('\n', ''):
                default_x = all_scheme[i-1]
            if all_scheme[i] == cfg_x[1].replace('\n', ''):
                secondary = all_scheme[i - 1]
            if all_scheme[i] == cfg_x[2].replace('\n', ''):
                game = all_scheme[i - 1]

        pro_array_hp = [x.lower() for x in p_a_hp]
        pro_array_b = [x.lower() for x in p_a_b]

        if not any(e in pro_array_hp for e in pro_array_b):
            switch = True
            curr_scheme = str(Popen('powercfg /GetActiveScheme', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE
                                    ).communicate()[0].decode("utf-8"))
            for process in pro_array_hp:
                after_process_search = "".join([s for s in process.strip().splitlines(True) if s.strip("\r\n").strip()])
                process_search = after_process_search in (i.name().lower() for i in psutil.process_iter())
                pro_hp.append(process_search)

            for process in pro_array_b:
                after_process_search = "".join([s for s in process.strip().splitlines(True) if s.strip("\r\n").strip()])
                process_search = after_process_search in (i.name().lower() for i in psutil.process_iter())
                pro_b.append(process_search)

            if cfg_x[2].replace('\n', '') not in curr_scheme:
                if True in pro_hp:
                    Popen(game, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    curr_scheme = str(Popen('powercfg /GetActiveScheme', shell=True, stdin=PIPE, stdout=PIPE,
                                            stderr=PIPE).communicate()[0].decode("utf-8")).replace(')', '').split('(')
                    tray.ShowMessage('Active Power Plan!', curr_scheme)

            if cfg_x[1].replace('\n', '') not in curr_scheme:
                if True in pro_b:
                    Popen(secondary, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    curr_scheme = str(Popen('powercfg /GetActiveScheme', shell=True, stdin=PIPE, stdout=PIPE,
                                            stderr=PIPE).communicate()[0].decode("utf-8")).replace(')', '').split('(')
                    tray.ShowMessage('Active Power Plan!', curr_scheme)

            if cfg_x[0].replace('\n', '') not in curr_scheme:
                if True not in pro_hp and True not in pro_b:
                    Popen(default_x, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    curr_scheme = str(Popen('powercfg /GetActiveScheme', shell=True, stdin=PIPE, stdout=PIPE,
                                            stderr=PIPE).communicate()[0].decode("utf-8")).replace(')', '').split('(')
                    tray.ShowMessage('Active Power Plan!', curr_scheme)
        else:
            if switch:
                tray.ShowMessage('Duplicates!', 'Remove common apps!')

                switch = False


menu_def = ['', ['Edit', '---', '!'+default, '!'+first, '!'+second, 'Exit']]
tray = Sg.SystemTray(menu=menu_def)
tray.ShowMessage('Startup', 'Started')
# ip_check_thread = Thread(target=main)
# ip_check_thread.start()
while True:
    menu_item = tray.Read()
    if menu_item in ('Edit', Sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
        layout = [[Sg.Text('Default    First     Second')],
                  [Sg.Listbox(for_default, enable_events=True, key='-DEFAULT-'),
                   Sg.Listbox(for_default, enable_events=True, key='-FIRST-'),
                   Sg.Listbox(for_default, enable_events=True, key='-SECOND-')]]
        window = Sg.Window('Window Title', layout, finalize=True)
        while True:
            event, values, = window.Read()
            if event is None or event == 'Exit':
                m_vpn_switch = False
                break
            elif event == '-DEFAULT-':
                p1 = ''.join(open('scheme.txt', 'r').readlines()).split('\n')
                default = values['-DEFAULT-'][0]
                p1[0] = values['-DEFAULT-'][0]
                open('scheme.txt', 'w+').write('\n'.join(p1))

            elif event == '-FIRST-':
                p1 = ''.join(open('scheme.txt', 'r').readlines()).split('\n')
                first = values['-FIRST-'][0]
                p1[1] = values['-FIRST-'][0]
                open('scheme.txt', 'w+').write('\n'.join(p1))

            elif event == '-SECOND-':
                p1 = ''.join(open('scheme.txt', 'r').readlines()).split('\n')
                second = values['-SECOND-'][0]
                p1[2] = values['-SECOND-'][0]
                open('scheme.txt', 'w+').write('\n'.join(p1))
            tray.update(['', ['Edit', '---', '!'+default, '!'+first, '!'+second, 'Exit']])
            # tray.ShowMessage('Power Plan', 'Updated!!')
    elif menu_item == 'Exit':
        call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
        break
