import re
from getpass import getuser
from os import getpid, path
from smtplib import SMTP_SSL
from ssl import create_default_context
from subprocess import call, Popen, PIPE
from threading import Thread
from time import sleep
import base64
import getpass
import glob
import hashlib
import os

from subprocess import call, Popen, PIPE
from threading import Thread
import PySimpleGUI as Sg

import asyncio
from pyppeteer import launch

from PyPDF2 import PdfReader
from refextract import extract_references_from_file

from Essentials import essential
from main import select_ref
from os.path import isfile
from ReadPDF import extract_ref

if not isfile('./ref-data.txt'):
    open('ref-data.txt', 'w+')


def select_pdf():
    pdf_layout = []
    pdf_to_read = []
    essential()
    pdf_names = [i.replace('./pdf\\', '') for i in glob.glob("./pdf/*.pdf") if i]

    for i in range(len(pdf_names)):
        pdf_layout += [[Sg.Text('', size=(1, 1))], [Sg.Checkbox(pdf_names[i], enable_events=True, disabled=False, key=f'-check{i}-')]]

    layout = [[Sg.Column(pdf_layout, size=(590, 590), scrollable=True)], [Sg.Button('Continue', disabled=False, size=(60, 1))]]
    #
    window = Sg.Window("WoLvES 2.0", layout, resizable=False, finalize=True)
    while True:
        event, values = window.read()
        if event == Sg.WINDOW_CLOSED:
            window.close()
            # call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
            break
        elif event == 'Continue':
            for i in range(len(pdf_names)):
                window[f'-check{i}-'].update(disabled=True)
            window['Continue'].update(disabled=True)
            window.hide()
            ref_dat = []
            for pdf in pdf_names:
                references = []
                ref = extract_references_from_file(pdf)
                for i in ref:
                    if i['raw_ref'][0] not in references:
                        references.append(i['raw_ref'][0])

                f_ref, nf_ref, temp = [], [], []

                for line in references:
                    if line.endswith("."):
                        if bool(re.findall(r'\[\d+\]', line)):
                            for t in temp:
                                f_ref.append(t.strip())
                            temp.clear()
                        f_ref.append((" ".join(temp) + " " + line).strip() if temp else line.strip())
                        temp.clear()
                    else:
                        temp.append(line)

                for line in f_ref:
                    if [x for x in [re.findall(pattern, line) for pattern in
                                    [r'\(\d{4}, [A-Za-z]+\)', r'\([A-Za-z]+, \d{4}\)', r'\((\d{4})\)']] if x]:
                        if bool(re.findall(r'\[\d+\]', line)):
                            nf_ref.append(line)
                            temp.clear()
                        else:
                            nf_ref.append((" ".join(temp)).strip() if len(temp) == 0 else "".join(temp).strip())
                        temp.clear()
                        temp.append(line)
                    else:
                        if bool(re.findall(r'\[\d+\]', line)):
                            nf_ref.append(line)
                            temp.clear()
                        temp.append(line)

                nf_ref = [re.sub(r'\[\d+\]', '', x) for x in nf_ref if x]
                ref_dat.extend(nf_ref)
            open('ref-data.txt', 'w', encoding="utf-8").write('\n'.join(ref_dat))
            select_ref(ref_dat)

            window.close()
        for i in range(len(pdf_names)):
            if event == f'-check{i}-':
                if values[f'-check{i}-']:
                    pdf_to_read.append(pdf_names[i])
                else:
                    pdf_to_read.remove(pdf_names[i])


select_pdf()
