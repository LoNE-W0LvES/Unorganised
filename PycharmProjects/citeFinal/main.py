from RefWin import reference_window

from os.path import isfile, isdir
from os import mkdir
import glob
import os
import pandas as pd
from subprocess import call
import PySimpleGUI as Sg

from ReadPDF import read_pdf
from BrowserAuto import get_bib
from screeninfo import screeninfo

from check_db import check_ref
from gsheet import get_data

screen_info = screeninfo.get_monitors()
primary_screen = screen_info[0]

monitor_width, monitor_height = primary_screen.width, primary_screen.height
window_width = int(monitor_width * 0.3)
window_height = int(monitor_height * 0.3)

if not isfile('./scholar.bib'):
    open('scholar.bib', 'w+')

if not isdir('./pdf'):
    mkdir('./pdf')

if len(glob.glob("./pdf/*.pdf")) == 0:
    Sg.popup_error('Put pdf into pdf folder...!!')
    call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)

if not isdir('./downloads'):
    mkdir('./downloads')


df, ws, pos = get_data()


def main():
    global ref_cite
    pdf_layout, pdf_to_read = [], []
    pdf_names = [i.replace('./pdf\\', '') for i in glob.glob("./pdf/*.pdf") if i]

    for i in range(len(pdf_names)):
        pdf_layout += [[Sg.Text('', size=(1, 1))],
                       [Sg.Checkbox(pdf_names[i], enable_events=True, disabled=False, key=f'-check{i}-')]]

    layout = [[Sg.Column(pdf_layout, size=(window_width, window_height), scrollable=True)],
              [Sg.Button('Continue', disabled=False, size=(window_width - 5, 1))]]

    window = Sg.Window("WoLvES 2.0", layout, size=(window_width, window_height + 100), resizable=True, finalize=True)
    while True:
        event, values = window.read()
        if event == Sg.WINDOW_CLOSED:
            window.close()
            break
        elif event == 'Continue':
            for i in range(len(pdf_names)):
                window[f'-check{i}-'].update(disabled=True)
            window['Continue'].update(disabled=True)
            window.hide()
            r_df = read_pdf(pdf_name_list=pdf_to_read)
            ref_cite = reference_window(r_df)
            return ref_cite
        for i in range(len(pdf_names)):
            if event == f'-check{i}-':
                if values[f'-check{i}-']:
                    pdf_to_read.append(pdf_names[i])
                else:
                    pdf_to_read.remove(pdf_names[i])


if __name__ == '__main__':
    ref_cite = main()
    ref_browser = check_ref(ref_cite, df)
    get_bib(ref_browser, ws, pos)
    df, ws, pos = get_data()
    try:
        for ff in range(len(ref_cite)):
            ref = ref_cite['Reference'][ff]
            index_ref = df.loc[df['Reference'] == ref].index[0]
            bib = df['BibTex'][index_ref]
            if bib is None or not pd.notna(bib):
                Sg.popup_error("not found bib")
            else:
                new_bib = bib.replace("\\n", "\n")
                open('scholar.bib', 'a').write(new_bib)
    except IndexError:
        pass
    Sg.popup('Done.')
