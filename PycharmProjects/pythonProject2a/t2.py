import PySimpleGUI as sg
from psgtray import SystemTray


def main():
    menu = ['',
            ['Show Window', 'Hide Window', '---', '!Disabled Item', 'Change Icon', ['Happy', 'Sad', 'Plain'], 'Exit']]
    tooltip = 'Tooltip'

    layout = [[sg.Text('My PySimpleGUI Celebration Window - X will minimize to tray')],

              [sg.Multiline(size=(60, 10), reroute_stdout=False, reroute_cprint=True, write_only=False, key='-OUT-')],
              [sg.Button('Go'), sg.B('Hide Icon'), sg.B('Show Icon'), sg.B('Hide Window'), sg.Button('Exit')]]

    window = sg.Window('Window Title', layout, finalize=True, enable_close_attempted_event=True)

    tray = SystemTray(menu, single_click_events=False, window=window, tooltip=tooltip, icon=sg.DEFAULT_BASE64_ICON)
    tray.show_message('System Tray', 'System Tray Icon Started!')
    sg.cprint(sg.get_versions())
    while True:
        event, values = window.read()

        if event == tray.key:
            sg.cprint(f'System Tray Event = ', values[event], c='white on red')
            event = values[event]

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        sg.cprint(event, values)
        tray.show_message(title=event, message=values)

        if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()
        elif event in ('Hide Window', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            window.hide()
            tray.show_icon()

    tray.close()  # optional but without a close, the icon may "linger" until moused over
    window.close()


if __name__ == '__main__':
    main()