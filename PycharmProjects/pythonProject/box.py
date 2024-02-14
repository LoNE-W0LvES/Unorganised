import json
import os
from subprocess import call

import PySimpleGUI as Sg


def write_json(filename, json_data):
    if os.path.exists(filename) and open(filename).read() is not None:
        with open(filename) as fx:
            obj = json.load(fx)
        obj.append(json_data)
    else:
        obj = json_data
    with open(filename, "w+") as of:
        json.dump(obj, of)

def box(data_self):
    box_col = []
    box_loc = './Stuff/box.json'
    g = open(box_loc)
    data_box = json.load(g)
    for j in range(len(data_box)):
        box_col += [[Sg.Text(data_box[j]['box-id'], size=(12, 1), key=f'-b-id{j}-'),
                    Sg.Text(data_box[j]['box-size'], size=(12, 1), key=f'-b-size{j}-'),
                    Sg.Text(data_box[j]['box-price'], size=(12, 1), key=f'-b-price{j}-'),
                    Sg.Text(data_box[j]['uid'], size=(12, 1), key=f'-uid{j}-'),
                    Sg.Button('Buy Box', key=f'-se-save{j}-')]]

    add_box = [[Sg.Text("    Box ID               Box Size               Box Price                  User ID          ")], [Sg.Column(box_col)]]

    window_customer = Sg.Window("BoX", add_box, finalize=True)
    while True:
        event, values = window_customer.read()
        if event == Sg.WINDOW_CLOSED:
            call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
            break
        for j in range(len(data_box)):
            if event == f'-se-save{j}-':
                data_au = {
                    'box-id': data_box[j]['box-id'],
                    'box-size': data_box[j]['box-size'],
                    'box-price': data_box[j]['box-price'],
                    'uid': data_self['id'],
                    'Status': '',
                }
                write_json('./Stuff/boxR.json', data_au)


def box_stuff():
    print("box_stuff")

    box_col = [[Sg.InputText("Box ID", size=(12, 1), key='-b-id-'),
                Sg.InputText("Box Size", size=(12, 1), key='-b-size-'),
                Sg.InputText("Box price", size=(12, 1), key='-b-price-'),
                Sg.InputText("User ID", size=(12, 1), key='-uid-')]]

    add_box = [[Sg.Text("    Box ID               Box Size                  User ID          ")], [Sg.Column(box_col)],
               [Sg.Button("Add Box", size=(10, 1), visible=True)]]

    window_stuff = Sg.Window("Stuff", add_box, finalize=True)
    while True:
        event, values = window_stuff.read()
        if event == Sg.WINDOW_CLOSED:
            break
        elif event == 'Add Box':
            data_au = {
                'box-id': values['-b-id-'],
                'box-size': values['-b-size-'],
                'box-price': values['-b-price-'],
                'uid': values['-uid-'],
                'Status': '',
            }
            write_json('./Stuff/box.json', data_au)
            break


def box_req():
    box_col = []
    box_loc = './Stuff/boxR.json'
    g = open(box_loc)
    data_box = json.load(g)
    for j in range(len(data_box)):
        if data_box[j]['Status'] != 'Approved':
            box_col += [[Sg.Text(data_box[j]['box-id'], size=(12, 1), key=f'-b-id{j}-'),
                        Sg.Text(data_box[j]['box-size'], size=(12, 1), key=f'-b-size{j}-'),
                        Sg.Text(data_box[j]['box-price'], size=(12, 1), key=f'-b-price{j}-'),
                        Sg.Text(data_box[j]['uid'], size=(12, 1), key=f'-uid{j}-'),
                        Sg.Button('Accept', key=f'Accept{j}')]]

    add_box = [
        [Sg.Text("    Box ID               Box Size               Box Price                  User ID          ")],
        [Sg.Column(box_col)]]

    window_customer = Sg.Window("BoX", add_box, finalize=True)
    while True:
        event, values = window_customer.read()
        if event == Sg.WINDOW_CLOSED:
            call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
            break
        for j in range(len(data_box)):
            if event == f'Accept{j}':
                data_au = {
                    'box-id': data_box[j]['box-id'],
                    'box-size': data_box[j]['box-size'],
                    'box-price': data_box[j]['box-price'],
                    'uid': data_box[j]['uid'],
                    'Status': "Approved",
                }
                write_json('./Stuff/boxR.json', data_au)