import json
import os
import threading
from datetime import datetime, timedelta
from subprocess import call
import PIL
from PIL import Image
import io
import base64
import os
import PySimpleGUI as Sg
from box import box_stuff, box_req
from mail import send_mail

stuff_loc = './Stuff/stuff.json'
f = open(stuff_loc)
data_stuff = json.load(f)
data_customer = []
for i in data_stuff:
    if i['User type'] == 'Stuff':
        data_customer.append(i)

for i in data_stuff:
    if i['User type'] == 'Customer':
        data_customer.append(i)


with open(stuff_loc, "w+") as of:
    json.dump(data_customer, of)

f = open(stuff_loc)
data_stuff = json.load(f)

data_customer = []

box_loc = './Stuff/box.json'
g = open(box_loc)
if g.read() == '':
    json.dump({"box-id": "", "box-size": "", "uid": ""}, g)
    g.close()
g = open(box_loc)
data_box = json.load(g)

THUMBNAIL_SIZE = (200, 200)
IMAGE_SIZE = (800, 800)

exp_date = []


def write_json(filename, json_data):
    if os.path.exists(filename) and open(filename).read() is not None:
        with open(filename) as fx:
            obj = json.load(fx)
        obj.append(json_data)
    else:
        obj = json_data
    with open(filename, "w+") as of:
        json.dump(obj, of)


def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im


def convert_to_bytes(file_or_bytes, resize=None, fill=False):
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            print(e)
            data_bytes_io = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(data_bytes_io)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height / cur_height, new_width / cur_width)
        img = img.resize((int(cur_width * scale), int(cur_height * scale)), PIL.Image.ANTIALIAS)
    if fill:
        img = make_square(img, THUMBNAIL_SIZE[0])
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()


def open_image(filename):
    try:
        layout = [[Sg.Image(data=convert_to_bytes(filename, IMAGE_SIZE), enable_events=True)]]
        eve, val = Sg.Window('Image', layout, modal=True, element_padding=(0, 0), margins=(0, 0)).read(close=True)
    except Exception as e:
        print(f'** Display image error **', e)
        Sg.popup(f'** Display image error **', e, title='File Not Found')
        return


def stuff():
    stuff_col = []
    box_col = []
    t_color = 'black'
    for j in range(len(data_stuff)):
        br_date = data_stuff[j]["Borrowed Date"].split('/')
        try:
            date_time = datetime(br_date[0], br_date[1], br_date[2])
            delta = date_time + timedelta(days=300)
            exp_d_v = delta - datetime.now()
        except:
            exp_d_v = 0
            if exp_d_v <= 30:
                t_color = 'red'
        exp_date.append(exp_d_v)
        stuff_col += [[Sg.DropDown(['Customer', 'Stuff'], default_value=data_stuff[j]['User type'], key=f'-se-user{j}-'),
                       Sg.InputText(data_stuff[j]['id'], size=(12, 1), key=f'-se-id{j}-'),
                       Sg.InputText(data_stuff[j]['Name'], size=(12, 1), key=f'-se-name{j}-'),
                       Sg.InputText(data_stuff[j]['phone'], size=(12, 1), key=f'-se-phone{j}-'),
                       Sg.InputText(data_stuff[j]['Email'], size=(12, 1), key=f'-se-mail{j}-'),
                       Sg.InputText(data_stuff[j]['password'], size=(12, 1), key=f'-se-pass{j}-'),
                       Sg.InputText(data_stuff[j]['address'], size=(12, 1), key=f'-se-address{j}-'),
                       Sg.DropDown(['Male', 'Female'], default_value=data_stuff[j]['Gender'], key=f'-se-gender{j}-'),
                       Sg.InputText(data_stuff[j]['Hair color'], size=(12, 1), key=f'-se-hc{j}-'),
                       Sg.InputText(data_stuff[j]['Eye color'], size=(12, 1), key=f'-se-ec{j}-'),
                       Sg.InputText(data_stuff[j]['Height'], size=(12, 1), key=f'-se-h{j}-'),
                       Sg.InputText(data_stuff[j]['Weight'], size=(12, 1), key=f'-se-w{j}-'),
                       Sg.InputText(data_stuff[j]['Box quantity'], size=(12, 1), key=f'-se-bq{j}-'), Sg.Text("    "),
                       Sg.Button('Open', key=f'-se-o-bl{j}-'), Sg.Text("       "),
                       Sg.Button('Open', key=f'-se-o-pap{j}-'), Sg.Text("         "),
                       Sg.Button('Open', key=f'-se-o-sig{j}-'), Sg.Text("     "),
                       Sg.Button('Open', key=f'-se-o-nid{j}-'), Sg.Text("      "),
                       Sg.Text(exp_d_v, size=(12, 1), text_color=t_color, justification='c', key=f'-se-expire{j}-'),
                       Sg.Button('Send Mail', key=f'-se-s-mail{j}-'),
                       Sg.Button('Save', key=f'-se-save{j}-')]]
    stuff_list = [[Sg.Text("    User Type               ID                  Name                Phone                "
                           "Email             Password           Address           Gender         Eye color           "
                           "Hair color             Height               Weight        Box Quantity           "
                           "Box Lists      Passport Photo      Signature            NID                       Expire")],
                  [Sg.Column(stuff_col)]]

    file_pass = [[Sg.Text(" "), Sg.FileBrowse(file_types=(("jpg File", "*.jpg"),
                                                          ("png File", "*.png")), key='file-passport')]]
    file_sig = [[Sg.Text(" "), Sg.FileBrowse(file_types=(("jpg File", "*.jpg"),
                                                         ("png File", "*.png")), key='file-signature')]]
    file_nid = [[Sg.Text(" "), Sg.FileBrowse(file_types=(("jpg File", "*.jpg"), ("png File", "*.png")), key='file-nid')]]

    for j in range(len(data_box)):
        box_col += [[Sg.InputText(data_box[j]['box-id'], size=(12, 1), key=f'-b-id{j}-'),
                     Sg.InputText(data_box[j]['box-size'], size=(12, 1), key=f'-b-size{j}-'),
                     Sg.InputText(data_box[j]['box-size'], size=(12, 1), key=f'-b-price{j}-'),
                     Sg.InputText(data_box[j]['uid'], size=(12, 1), key=f'-uid{j}-'),
                     Sg.Button('Save Box', key=f'-se-save{j}-')]]

    add_box = [[Sg.Text("    Box ID               Box Size                  User ID          ")], [Sg.Column(box_col)],
               [Sg.Button("Add Box", size=(10, 1), visible=True)], [Sg.Button("Box Request", size=(10, 1), visible=True)]]

    add_user = [[Sg.Text("                            Add User                            ", font='Any 25')],
                [Sg.Text(" ")],
                [Sg.Text("User ", size=(13, 1), font='Any 10'),
                 Sg.DropDown(['Customer', 'Stuff'], default_value='Customer', key='-select-user-'),
                 Sg.Button("Select User", size=(10, 1))],
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
                [Sg.Text(" ")],
                [Sg.Button("Add User", size=(10, 1), visible=True)]]

    tab_group_eu = [[Sg.Tab('                              Stuff List                                ',
                            stuff_list, font='Courier 15', key='-SL-')]]

    user_list = [[Sg.TabGroup(tab_group_eu)]]

    tab_group_s = [[Sg.Tab('                              Add User                               ',
                           add_user, font='Courier 15', key='-TAB1-'),
                    Sg.Tab('                              Add Box                                ',
                           add_box, visible=True, key='-TAB2-'),
                    Sg.Tab('                             User List                               ',
                           user_list, visible=True, key='-TAB3-')]]

    layout_stuff = [[Sg.TabGroup(tab_group_s, title_color='#0f0f0f', enable_events=True, key='-TAB-S-')],
                    [Sg.Text("", size=(20, 1), font='Any 8', key='status')]]
    window_stuff = Sg.Window("Stuff", layout_stuff, finalize=True)
    while True:
        event, values = window_stuff.read()
        if event == Sg.WINDOW_CLOSED:
            call('taskkill.exe /F /IM ' + str(os.getpid()), shell=True)
            break
        elif event == 'Add User':
            data_au = {
                "User type": values['-select-user-'],
                "id": values['-st-t-'] if values['-select-user-'] == 'Stuff' else values['-phone-'],
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
                "Box quantity": '',
                "Borrowed Date": '',
                "Box Size": '',
                "Box Price": '',
                "Time Limit": ''
            }
            write_json(stuff_loc, data_au)
        elif event == 'Add Box':
            box_stuff()
        elif event == 'Box Request':
            box_req()
        for j in range(len(data_box)):
            data_au = {
                'box-id': values[f'-b-id{j}-'],
                'box-size': values[f'-b-size{j}-'],
                'box-price': values[f'-b-price{j}-'],
                'uid': values[f'-uid{j}-'],
                'Status': '',
            }
            write_json('./Stuff/box.json', data_au)

        for j in range(len(data_stuff)):
            if event == f'-se-o-pap{j}-':
                thread_x = threading.Thread(target=open_image(data_stuff[j]['id'] + '-passport.png'))
                thread_x.start()
            if event == f'-se-o-sig{j}-':
                thread_x = threading.Thread(target=open_image(data_stuff[j]['id'] + '-signature.png'))
                thread_x.start()
            if event == f'-se-o-nid{j}-':
                thread_x = threading.Thread(target=open_image(data_stuff[j]['id'] + '-nid.png'))
                thread_x.start()
            if event == f'-se-save{j}-':
                data = {
                    "User type": values[f'-se-user{j}-'],
                    "id": values[f'-se-id{j}-'],
                    "Name": values[f'-se-name{j}-'],
                    "phone": values[f'-se-phone{j}-'],
                    "Email": values[f'-se-mail{j}-'],
                    "password": values[f'-se-pass{j}-'],
                    "Gender": values[f'-se-gender{j}-'],
                    "Hair color": values[f'-se-hc{j}-'],
                    "Eye color": values[f'-se-ec{j}-'],
                    "Height": values[f'-se-h{j}-'],
                    "Weight": values[f'-se-w{j}-'],
                    "address": values[f'-se-address{j}-'],
                    "Box quantity": values[f'-se-bq{j}-'],
                    "Borrowed Date": '',
                    "Box Size": '',
                    "Box Price": '',
                    "Time Limit": ''
                }
                data_stuff[j] = data
                with open(stuff_loc, "w+") as ofx:
                    json.dump(data_stuff, ofx)
            if event == f'-se-s-mail{j}-':
                send_mail(values[f'-se-mail{j}-'], exp_date[j])

