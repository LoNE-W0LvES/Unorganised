import json
import os
from subprocess import call

import PySimpleGUI as Sg
from box import box

def customer(data_self):
    print(data_self)
    if os.path.exists(data_self['id'] + '.jpg'):
        file_name = data_self['id'] + '.jpg'
    elif os.path.exists(data_self['id'] + '.png'):
        file_name = data_self['id'] + '.png'
    else:
        file_name = 'default.png'

    box_col = []
    box_loc = './Stuff/boxR.json'
    g = open(box_loc)
    data_box = json.load(g)
    for j in range(len(data_box)):
        if data_box[j]['Status'] == 'Approved' and data_self['id'] == data_box[j]['uid']:
            box_col += [[Sg.Text(data_box[j]['box-id'], size=(12, 1), key=f'-b-id{j}-'),
                        Sg.Text(data_box[j]['box-size'], size=(12, 1), key=f'-b-size{j}-'),
                        Sg.Text(data_box[j]['box-price'], size=(12, 1), key=f'-b-price{j}-'),
                        Sg.Text(data_box[j]['uid'], size=(12, 1), key=f'-uid{j}-')], [Sg.Button('Remove Box', key=f'rbox{j}')]]

    box_user = [
        [Sg.Text("    Box ID               Box Size               Box Price                  User ID          ")],
        [Sg.Column(box_col)]]

    app_rent = [[Sg.Text("                                                Rent                                            ", font='Any 25')],
                  [Sg.Button('See Box')]
                  ]
    payment = [[]]
    my_profile = [[Sg.Text("                                          My Profile                                          ", font='Any 25')],
                  [Sg.Image(file_name, size=(200, 200))], [Sg.Column(box_user)], [Sg.Button('Visit Box', key=f'-vb-')]
                  ]
    tab_group_c = [[Sg.Tab('                           Apply for rent                            ',
                           app_rent, font='Courier 15', key='-TAB1-'),
                    Sg.Tab('                              payment                                ',
                           payment, visible=True, key='-TAB2-'),
                    Sg.Tab('                             My Profile                              ',
                           my_profile, visible=True, key='-TAB2-')]]

    layout_customer = [[Sg.TabGroup(tab_group_c, title_color='#0f0f0f', enable_events=True, key='-TAB-C-')],
                       [Sg.Text("", size=(20, 1), font='Any 8', key='status')]]

    window_customer = Sg.Window("Customer", layout_customer, finalize=True)
    while True:
        event, values = window_customer.read()
        if event == Sg.WINDOW_CLOSED:
            call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
            break
        elif event == 'See Box':
            box(data_self)

    # customer()


    # window_customer = Sg.Window("BoX", add_box, finalize=True)
    # while True:
    #     event, values = window_customer.read()
    #     if event == Sg.WINDOW_CLOSED:
    #         call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
    #         break
    #     for j in range(len(data_box)):
    #         if event == f'Accept{j}':
    #             data_au = {
    #                 'box-id': values[f'-b-id{j}-'],
    #                 'box-size': values[f'-b-size{j}-'],
    #                 'box-price': values[f'-b-price{j}-'],
    #                 'uid': values[f'-uid{j}-'],
    #                 'Status': 'Approved',
    #             }
    #             write_json('./Stuff/boxR.json', data_au)
