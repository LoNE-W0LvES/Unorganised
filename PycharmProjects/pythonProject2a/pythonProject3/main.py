import random
import PySimpleGUIQt as Sg
import os

Custom_Visibility = False
if not os.path.isfile('Custom.txt'):
    open('Custom.txt', "w+")
    Sg.popup_ok("Add names to Custom.txt")


with open('Custom.txt') as file:
    lines = len(file.readlines())
if lines != 0:
    Custom_Visibility = True


Pistol = ["Classic", "Shorty", "Frenzy", "Ghost", "Sheriff"]

Half_Eco = ["Sheriff", "Stinger", "Spectre", "Bucky", "Judge", "Marshal", "Ares"]

Full_Buy = ["Stinger", "Spectre", "Bucky", "Judge", "Bulldog", "Guardian", "Phantom", "Vandal", "Marshal", "Operator", "Ares", "Odin"]

All_Weapon = ["Classic", "Shorty", "Frenzy", "Ghost", "Sheriff", "Stinger", "Spectre", "Bucky", "Judge", "Bulldog", "Guardian", "Phantom", "Vandal", "Marshal", "Operator", "Ares", "Odin"]

layout_0 = [
    [
        Sg.Text("Select A Option", text_color='black', key="-Weapon-")
    ],
    ]
layout_1 = [
    [
        Sg.Button('Pistol', size=(15, 1))
    ],
    ]
layout_2 = [
    [
        Sg.Button('Half Eco', size=(15, 1))
    ],
    ]
layout_3 = [
    [
        Sg.Button('Full Buy', size=(15, 1))
    ],
    ]
layout_4 = [
    [
        Sg.Button('All Weapon', size=(15, 1))
    ],
    ]
layout_5 = [
    [
        Sg.Button('Custom', size=(15, 1))
    ],
]

layout = [
    [
        Sg.Column(layout_0, element_justification='l')
    ],
    [
        Sg.Column(layout_1, element_justification='c')
    ],
    [
        Sg.Column(layout_2, element_justification='c')
    ],
    [
        Sg.Column(layout_3, element_justification='c')
    ],
    [
        Sg.Column(layout_4, element_justification='c')
    ],
    [
        Sg.Column(layout_5, element_justification='c', visible=Custom_Visibility, key='custom-key')
    ],
]

window = Sg.Window('Window Title', layout, size=(300, 300), finalize=True)

while True:
    event, values = window.Read()
    if event == Sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Pistol':
        WeaponName = random.choice(Pistol)
        window["-Weapon-"].Update("Random Weapon:  " + WeaponName)

    if event == 'Half Eco':
        WeaponName = random.choice(Half_Eco)
        window["-Weapon-"].Update("Random Weapon:  " + WeaponName)

    if event == 'Full Buy':
        WeaponName = random.choice(Full_Buy)
        window["-Weapon-"].Update("Random Weapon:  " + WeaponName)

    if event == 'All Weapon':
        WeaponName = random.choice(All_Weapon)
        window["-Weapon-"].Update("Random Weapon:  " + WeaponName)

    if event == 'Custom':
        with open("Custom.txt", 'r') as filex:
            read_Custom = filex.readlines()
            filex.close()
        WeaponName = random.choice(read_Custom).replace('\n', '')
        window["-Weapon-"].Update("Random Weapon:  " + WeaponName)

