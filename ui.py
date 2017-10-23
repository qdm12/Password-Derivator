from passgen import passgen, MasterPasswordDigestException
from setup import setup, check_birthdate, check_master_password

from kivy.app import App  
from kivy.uix.popup import Popup  
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.button import Button


class Dimensions(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def tuplize(self):
        return (self.width, self.height)

class PassGenScreen(Screen):#BoxLayout
    def on_pre_enter(self):
        self.ids["PassGenButton"].state = "down"
        
    def on_submit_website(self, text_input):
        try:
            password = passgen(text_input) # show loading animation
        except MasterPasswordDigestException as e:
            self.ids["new_password"].text = "Your new password"
            box = BoxLayout(orientation="vertical")
            pop_up_dim = Dimensions(0.8, 0.5)
            label = Label(text="An error occurred when reading the Master Password Digest file ({}). You might want to re-run SETUP".format(str(e)),
                         text_size=(pop_up_dim.width * self.width, pop_up_dim.height * self.height),
                         halign="center", valign="middle")
            subbox = BoxLayout(orientation="horizontal", spacing=0.1*self.width, padding=(0.05*self.width, 0.1*self.height))
            button_setup = Button(text="Setup", font_size=15, size_hint=(0.4,0.4))
            button_close = Button(text="Close", font_size=15, size_hint=(0.4,0.4))
            subbox.add_widget(button_setup)
            subbox.add_widget(button_close)
            
            
            box.add_widget(label)
            box.add_widget(subbox)
            
            pop_up = Popup(title="File Reading error",
                           content=box,
                           size_hint=pop_up_dim.tuplize())

            pop_up.open()
        else:
            self.ids["new_password"].text = password

class SetupScreen(Screen):
    def on_pre_enter(self):
        self.ids["SetupButton"].state = "down"

class SettingsScreen(Screen):  
    def on_pre_enter(self):
        self.ids["SettingsButton"].state = "down"

class ToolsScreen(Screen):  
    def on_pre_enter(self):
        self.ids["ToolsButton"].state = "down"


class DerivatexApp(App):  
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(PassGenScreen(name='PassGen')) 
        sm.add_widget(SetupScreen(name='Setup'))
        sm.add_widget(SettingsScreen(name='Settings'))
        sm.add_widget(ToolsScreen(name='Tools'))
        sm.current = 'PassGen'
        return sm

if __name__ == "__main__":  
    Config.set('graphics', 'width', '384')
    Config.set('graphics', 'height', '681')
    DerivatexApp().run()