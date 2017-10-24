from passgen import passgen, MasterPasswordDigestException, isMasterpassworddigestfilePresent
from setup import setup, check_master_password

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
        self.ids["SetupButton"].state = "normal"

    def on_submit_website(self, text_input):
        if text_input == "":
            self.ids["new_password"].text = "Your new password"
            box = BoxLayout(orientation="vertical")
            box.padding = (0.1*box.width, 0.1*box.height)
            pop_up_dim = Dimensions(0.6, 0.5)
            pop_up_text_dim = Dimensions(0.5, 0.5)
            label = Label(text="Please enter a valid website or company name",
                          text_size=(pop_up_text_dim.width * self.width, pop_up_text_dim.height * self.height),
                          halign="center", valign="middle")
            box.add_widget(label)
            
            subbox = BoxLayout()
            subbox.padding = (0.1*subbox.width, 0.1*subbox.height)
            button_close = Button(text="Close", font_size=15, size_hint=(0.5,0.6))
            subbox.add_widget(button_close)
            box.add_widget(subbox)
            
            pop_up = Popup(title="Website/Company name",
                           content=box,
                           size_hint=pop_up_dim.tuplize())
            button_close.bind(on_press=lambda x:pop_up.dismiss())
            pop_up.open()
            return
        try:
            password = passgen(text_input) # show loading animation
        except MasterPasswordDigestException as e:
            self.ids["new_password"].text = "Your new password"
            box = BoxLayout(orientation="vertical")
            pop_up_dim = Dimensions(0.8, 0.5)
            pop_up_text_dim = Dimensions(0.7, 0.5)
            
            label = Label(text="An error occurred when reading the Master Password Digest file ({}). You might want to re-run SETUP".format(str(e)),
                         text_size=(pop_up_text_dim.width * self.width, pop_up_text_dim.height * self.height),
                         halign="center", valign="middle")
            subbox = BoxLayout(orientation="horizontal")
            subbox.spacing = 0.2*subbox.width
            subbox.padding = (0.1*subbox.width, 0.1*subbox.height)
            button_setup = Button(text="Setup", font_size=15, size_hint=(0.4,0.4))
            button_close = Button(text="Close", font_size=15, size_hint=(0.4,0.4))
            subbox.add_widget(button_setup)
            subbox.add_widget(button_close)
            box.add_widget(label)
            box.add_widget(subbox)
            pop_up = Popup(title="File Reading error",
                           content=box,
                           size_hint=pop_up_dim.tuplize())
            button_setup.bind(on_press=lambda x:self._go_setup(pop_up))
            button_close.bind(on_press=lambda x:pop_up.dismiss())
            pop_up.open()
        else:
            self.ids["new_password"].text = password
            
    def _go_setup(self, pop_up):
        pop_up.dismiss()
        self.manager.current='Setup'

class SetupScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(SetupScreen, self).__init__(*args, **kwargs)
        self.pop_up = None
        self.p1 = None
        self.p2 = None
        self.birthdate = None
        
    def on_pre_enter(self):
        self.ids["PassGenButton"].state = "normal"
        self.ids["SetupButton"].state = "down"
    
    def customPopUp(self, title, message, text1, binding1, text2=None, binding2=None):
        box = BoxLayout(orientation="vertical")
        pop_up_dim = Dimensions(0.8, 0.5)
        pop_up_text_dim = Dimensions(0.7, 0.5)
        
        label = Label(text=message,
                     text_size=(pop_up_text_dim.width * self.width, pop_up_text_dim.height * self.height),
                     halign="center", valign="middle")
        subbox = BoxLayout(orientation="horizontal")
        subbox.spacing = 0.2*subbox.width
        subbox.padding = (0.1*subbox.width, 0.1*subbox.height)
        button1 = Button(text=text1, font_size=15, size_hint=(0.4,0.4))
        subbox.add_widget(button1)
        if text2 is not None:
            button2 = Button(text=text2, font_size=15, size_hint=(0.4,0.4))
            subbox.add_widget(button2)
        box.add_widget(label)
        box.add_widget(subbox)
        self.pop_up = Popup(title=title, content=box,
                            size_hint=pop_up_dim.tuplize())
        button1.bind(on_press=binding1)
        if binding2 is not None:
            button2.bind(on_press=binding2)
        self.pop_up.open()        
        
    def on_submit_credentials(self, master_password1, master_password2, day, month, year):
        # Process the birth date first
        if day == "Day" or month == "Month" or year == "Year":
            self.customPopUp("Birthdate missing",
                             "Please enter all the fields for your birthdate and try again", 
                             "Close", self._close)
            return
        day = day if len(day) == 2 else '0' + day
        month = month if len(month) == 2 else '0' + month
        self.birthdate = str(day) + '/' + str(month) + '/' + str(year)
        self.p1 = master_password1
        self.p2 = master_password2
        if isMasterpassworddigestfilePresent():
            self.customPopUp("Digest file exists",
                             "Master password digest secured file already exists. Would you like to overwrite it?", 
                             "Overwrite", self._overwrite_go_part1,
                             "Abort", self._close)
        else:
            self.continue_part1()
        
    def continue_part1(self):
        valid, safer, message = check_master_password(self.p1, self.p2)
        print(message)
        if not valid:
            self.customPopUp("Invalid password",
                             message,
                             "Close", self._close)
        elif not safer:
            self.customPopUp("Password has a weak security",
                             message,
                             "Enter again", self._close,
                             "Continue", self._close_go_part2)        
        else:
            self.continue_part2()
        
    def continue_part2(self):
        self.p2 = None
        success, message = setup(self.p1, self.birthdate) # show loading
        print(message)
        if success:
            self.customPopUp("Success",
                             message,
                             "Close", self._close_clean_success)
        else:
            self.customPopUp("File generation error",
                             message + " Would you like to try the generation again ?",
                             "Yes", self._close_go_part2,
                             "Abort", self._close_clean)
    
    def _close(self, pop_up):
        self.pop_up.dismiss()
            
    def _overwrite_go_part1(self, pop_up):
        self._close(pop_up)
        self.continue_part1()
        
    def _close_go_part2(self, pop_up):
        self._close(pop_up)
        self.continue_part2()
        
    def _close_clean(self, pop_up):
        self.p1 = self.p2 = self.birthdate = None
        self.ids["master_password1"] = self.ids["master_password2"] = ""
        self.ids["day"] = "Day"
        self.ids["month"] = "Month"
        self.ids["year"] = "Year"
        self._close(pop_up)
        
    def _close_clean_success(self, pop_up):
        self._close_clean(pop_up)
        self.manager.current = 'PassGen'

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
        if not isMasterpassworddigestfilePresent():
            sm.current = 'Setup'
        else:
            sm.current = 'PassGen'
        return sm

if __name__ == "__main__":  
    Config.set('graphics', 'width', '384')
    Config.set('graphics', 'height', '681')
    DerivatexApp().run()