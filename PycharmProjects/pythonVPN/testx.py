import PySimpleGUIQt as Sg

def login():
    # global username, password, line_count
    # Sg.theme(theme)

    login_button = [
        [Sg.Button("Login", size=(10, 1), visible=True), ]
    ]
    layout = [[Sg.Text("Log In", justification='center', font='Any 25')],
              [Sg.Text("Username", size=(10, 1), font='Any 15'),
               Sg.InputText(key='-usrnm-', size=(21, 1), font='Any 15')],
              [Sg.Text("Password", size=(10, 1), font='Any 15'),
               Sg.InputText(key='-pwd-', password_char='*', size=(21, 1), font='Any 15')],
              [Sg.Column(login_button, element_justification='r')]
              ]

    window = Sg.Window("Change Log In", layout, icon='./Essentials/app.ico', default_element_size=(15, 1),
                       resizable=False, grab_anywhere=True,
                       no_titlebar=False)

    while True:
        event, values = window.read()
        if event == Sg.WIN_CLOSED:
            exit()
        elif event == "Login":
            username = values['-usrnm-']
            password = values['-pwd-']
            file = open("./Essentials/myauthfile.txt", "w")
            file.write(username + "\n")
            file.close()
            file = open("./Essentials/myauthfile.txt", "a")
            file.write(password + "\n")
            file.close()
            Sg.popup("Username and Password Updated...")
            break
    window.close()
lo