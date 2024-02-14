import getpass
import math
import os
import re
import sys
import time
from pathlib import Path
from subprocess import Popen, PIPE
from threading import Thread

import PySimpleGUIQt as Sg
import psutil
from win32com.client import Dispatch


def multiple_replace(string, rep_dict):
    pat = re.compile("|".join([re.escape(str(k)) for k in sorted(rep_dict, key=len, reverse=True)]), flags=re.DOTALL)
    return pat.sub(lambda x: rep_dict[x.group(0)], string)


s_call = Popen('powercfg /list', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()[0].decode("utf-8")
replacing = multiple_replace(s_call, {'Power Scheme GUID:': 'powercfg /setactive', ')': '', ' *': '', '  (': '+'})
all_scheme = '+'.join(replacing.split('\r\n')[3:-1]).split('+')
for_default = for_first = for_second = [all_scheme[(i*2)+1] for i in range(math.floor(len(all_scheme)/2))]


f_n_hp = 'processHP.txt'
f_n_b = 'processB.txt'
user_name = getpass.getuser()
new_name = Path(os.path.basename(sys.argv[0])).resolve().stem
if not os.path.isfile(f_n_b):
    open(f_n_b, "w+")
if not os.path.isfile(f_n_hp):
    open(f_n_hp, "w+")
if not os.path.isfile('scheme.txt'):
    open('scheme.txt', "w+").write('\n\n\n')


path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\%s.lnk' % (user_name, new_name)
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = r"%s\%s" % (os.getcwd(), os.path.basename(sys.argv[0]))
shortcut.WorkingDirectory = os.getcwd()
shortcut.save()


def kill_switch():
    switch = True
    while True:
        pro_b = []
        pro_hp = []
        p_a_b = []
        p_a_hp = []
        default = ''
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

        cfg = open('scheme.txt', 'r').readlines()

        for i in range(len(all_scheme)):
            if all_scheme[i] == cfg[0].replace('\n', ''):
                default = all_scheme[i-1]
            if all_scheme[i] == cfg[1].replace('\n', ''):
                secondary = all_scheme[i - 1]
            if all_scheme[i] == cfg[2].replace('\n', ''):
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

            if cfg[2].replace('\n', '') not in curr_scheme:
                if True in pro_hp:
                    Popen(game, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    new_scheme = str(Popen('powercfg /GetActiveScheme', shell=True, stdin=PIPE, stdout=PIPE,
                                           stderr=PIPE).communicate()[0].decode("utf-8"))
                    print(new_scheme)

            if cfg[1].replace('\n', '') not in curr_scheme:
                if True in pro_b:
                    Popen(secondary, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    new_scheme = str(Popen('powercfg /GetActiveScheme', shell=True, stdin=PIPE, stdout=PIPE,
                                           stderr=PIPE).communicate()[0].decode("utf-8"))
                    print(new_scheme)

            if cfg[0].replace('\n', '') not in curr_scheme:
                if True not in pro_hp and True not in pro_b:
                    Popen(default, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
                    new_scheme = str(Popen('powercfg /GetActiveScheme', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE
                                           ).communicate()[0].decode("utf-8"))
                    print(new_scheme)
        else:
            if switch:
                Sg.popup('Remove common apps')
                switch = False


ip_check_thread = Thread(target=kill_switch)
ip_check_thread.start()


menu_def = ['BLANK', ['&Open', '---', '&Default::key=def', for_default, '&First state', for_first, '&Second state', for_second, 'E&xit']]

tray = Sg.SystemTray(menu=menu_def)

while True:  # The event loop
    event = tray.Read()
    if event == 'Exit':
        break
    elif event == 'def':
        print('event')
