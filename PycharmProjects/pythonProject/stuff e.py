# from datetime import date, datetime, timedelta
#
# date_time = datetime(2022, 11, 6)
#
# delta = date_time + timedelta(days=300)
#
# exp_date = delta - datetime.now()
#
#
# # d0 = datetime(int(date_time[0]), int(date_time[1]), int(date_time[2]), int(date_time[3]), int(date_time[4]), int(date_time[5]))
# # d1 = date(int(date_time[0]), int(date_time[1]), int(date_time[2]))
#
# # print(date_time.day)        # 25
# # print(date_time.month)      # 5
# # print(date_time.year)       # 2021
# # print(date_time.hour)       # 11
# # print(date_time.minute)     # 22
# # print(date_time.second)     # 3
#
# print(exp_date.days)
#
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

box_col = []
box_loc = './Stuff/box.json'
g = open(box_loc)
data_box = json.load(g)
print(data_box)
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
                'box-id': values[f'-b-id{j}-'],
                'box-size': values[f'-b-size{j}-'],
                'box-price': values[f'-b-price{j}-'],
                'uid': '',
                'Status': '',
            }
            write_json('./Stuff/boxR.json', data_au)