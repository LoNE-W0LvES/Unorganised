from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_string('''
<RootWidget>:
    manager: manager
    do_default_tab: False
    # add a ScreenManager to the panel
    ScreenManager:
        id: manager
        Screen:
            id: sc1
            name: 'screen_one'
            Button:
                text: 'screen one'
        Screen
            id: sc2
            name: 'screen_two'
            Button:
                text: 'Screen Two'
        Screen:
            id: sc3
            name: 'screen_three'
            Button:
                text: 'screen three'
    TabbedPanelHeader:
        text: sc1.name
        # store a screen name to link the tab to a screen
        screen: sc1.name
    TabbedPanelHeader:
        text: sc2.name
        screen: sc2.name
    TabbedPanelHeader:
        text: sc3.name
        screen: sc3.name
''')

class RootWidget(TabbedPanel):

    manager = ObjectProperty(None)

    def switch_to(self, header):
        # set the Screen manager to load  the appropriate screen
        # linked to the tab head instead of loading content
        self.manager.current = header.screen
        # we have to replace the functionality of the original switch_to
        self.current_tab.state = "normal"
        header.state = 'down'
        self._current_tab = header

class MainApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainApp().run()