import glob
import PySimpleGUI as Sg
from os.path import isfile, isdir
from os import mkdir


def essential():
    if not isdir('./pdf'):
        mkdir('./pdf')

    if not isfile('./ref-data.txt'):
        open('ref-data.txt', 'w+')

    if len(glob.glob("./pdf/*.pdf")) == 0:
        Sg.popup_error('Put pdf into pdf folder...!!')
