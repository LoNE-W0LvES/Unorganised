
import os
import pandas as pd
from subprocess import call
import PySimpleGUI as Sg
from screeninfo import screeninfo


def reference_window(ref_data):
    screen_info = screeninfo.get_monitors()
    primary_screen = screen_info[0]

    # Calculate the size of the window based on the monitor's resolution
    monitor_width, monitor_height = primary_screen.width, primary_screen.height
    window_width = int(monitor_width * 0.8)  # Adjust as needed
    window_height = int(monitor_height * 0.8)  # Adjust as needed
    ref_layout = []
    sw = True
    ref_to_cite = pd.DataFrame(columns=['Reference', 'BibTex', 'EndNote', 'RefMan'])
    for i in range(len(ref_data)):
        ref_layout += [[Sg.Text('', size=(1, 1))],
                       [Sg.Checkbox(ref_data.get('Reference')[i], enable_events=True, disabled=False,
                                    key=f'-r-check{i}-')]]

    lay = [[Sg.Column(ref_layout, size=(window_width, window_height - 100), scrollable=True)],
           [Sg.Column([[Sg.Button('Select Inverse', size=(60, 1), disabled=False, key='inverse'),
                        Sg.Button('Select All', size=(60, 1), disabled=False, key='all'),
                        Sg.Button('Continue', size=(60, 1), disabled=False)]], vertical_alignment='center',
                      justification='center')]]
    w = Sg.Window("Cite", lay, size=(window_width, window_height), resizable=False, finalize=True)

    while True:
        e, v = w.read()
        if e == Sg.WINDOW_CLOSED:
            w.close()
            call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
            break
        elif e == 'Continue':
            for i in range(len(ref_data)):
                if v[f'-r-check{i}-']:
                    ref_to_cite = pd.concat([ref_to_cite, ref_data.iloc[[i]]], ignore_index=True)

            # for i in range(len(ref_data)):
            #     w[f'-r-check{i}-'].update(disabled=True)
            # w['Continue'].update(disabled=True)
            # w.hide()
            # print(ref_to_cite['Reference'].values)
            w.hide()
            return ref_to_cite
        elif e == 'all':
            for i in range(len(ref_data)):
                w[f'-r-check{i}-'].update(sw)
            w['all'].update('Deselect All' if sw else 'Select All')
            sw = not sw
        elif e == 'inverse':
            for i in range(len(ref_data)):
                w[f'-r-check{i}-'].update(not v[f'-r-check{i}-'])

    w.close()