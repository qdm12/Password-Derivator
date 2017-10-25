from passgen import passgen, MasterPasswordDigestException, isMasterpassworddigestfilePresent
from setup import setup, check_master_password, get_time_cost,\
    get_time_per_time_cost

from kivy.app import App  
from kivy.uix.popup import Popup  
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar

from threading import Thread
from time import time

TIME_PER_TIMECOST = 0.4 # slow device

class Dimensions(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def tuplize(self):
        return (self.width, self.height)

class PassGenScreen(Screen):#BoxLayout
    def __init__(self, *args, **kwargs):
        super(PassGenScreen, self).__init__(*args, **kwargs)
        self.pop_up = None
        
    def on_pre_enter(self):
        self.ids["PassGenButton"].state = "down"
        self.ids["SetupButton"].state = "normal"
        
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

    def on_submit_website(self, text_input):
        self.ids["new_password"].text = "Your new password"
        if text_input == "":
            self.customPopUp("Invalid website/company name",
                             "Please enter a valid website or company name", 
                             "Close", self._close_popup)
            return
        try:
            password = passgen(text_input) # show loading animation
        except MasterPasswordDigestException as e:
            self.customPopUp("File reading error",
                             "An error occurred when reading the Master Password Digest file ({}). You might want to re-run SETUP".format(str(e)), 
                             "Setup", self._close_go_setup,
                             "Close", self._close_popup)
        else:
            self.ids["new_password"].text = password
            
    def _close_popup(self, origin=None):
        self.pop_up.dismiss()
            
    def _close_go_setup(self, origin=None):
        self._close_popup()
        self.manager.current='Setup'

class SetupScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(SetupScreen, self).__init__(*args, **kwargs)
        self.pop_up = None
        self.p1 = None
        self.p2 = None
        self.birthdate = None
        self.progress = None
        global TIME_PER_TIMECOST
        
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
                             "Close", self._close_popup)
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
                             "Abort", self._close_popup)
        else:
            self.continue_part1()
        
    def continue_part1(self):
        valid, safer, message = check_master_password(self.p1, self.p2)
        print(message)
        if not valid:
            self.customPopUp("Invalid password",
                             message,
                             "Close", self._close_popup)
        elif not safer:
            self.customPopUp("Password has a weak security",
                             message,
                             "Enter again", self._close_popup,
                             "Continue", self._close_go_part2)        
        else:
            self.continue_part2()
        
    def continue_part2(self):
        self.p2 = None
        box = BoxLayout(orientation="vertical", padding=(0.1*self.width, 0.1*self.height))
        time_needed = get_time_cost(self.birthdate)
        self.progress = ProgressBar(max=time_needed)
        box.add_widget(self.progress)
        pop_up_dim = Dimensions(0.8, 0.5)
        self.pop_up = Popup(title="Computing file, please wait...",
                            content=box,
                            size_hint=pop_up_dim.tuplize())
        self.pop_up.open()
        progressthread = Thread(target=self.animate_progress)
        setupthread = Thread(target=self.continue_part3)
        progressthread.start()
        setupthread.start()
        
    def animate_progress(self):
        start = time()
        print("Using TIME_PER_TIMECOST: ", TIME_PER_TIMECOST)
        while self.pop_up is not None:
            self.progress.value = (time() - start) / TIME_PER_TIMECOST
        self.progress = None
            
    def continue_part3(self):
        success, message = setup(self.p1, self.birthdate)
        self._close_popup()
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
    
    def _close_popup(self, origin=None):
        self.pop_up.dismiss()
        self.pop_up = None
            
    def _overwrite_go_part1(self, origin=None):
        self._close_popup()
        self.continue_part1()
        
    def _close_go_part2(self, origin=None):
        self._close_popup()
        self.continue_part2()
        
    def _close_clean(self, origin=None):
        self.p1 = self.p2 = self.birthdate = None
        self.ids["master_password1"] = self.ids["master_password2"] = ""
        self.ids["day"] = "Day"
        self.ids["month"] = "Month"
        self.ids["year"] = "Year"
        self._close_popup()
        
    def _close_clean_success(self, origin=None):
        self._close_clean()
        self.manager.current = 'PassGen'

class SettingsScreen(Screen):  
    def on_pre_enter(self):
        self.ids["SettingsButton"].state = "down"

class ToolsScreen(Screen):  
    def on_pre_enter(self):
        self.ids["ToolsButton"].state = "down"

class DerivatexApp(App):    
    def find_performance_argon(self):
        global TIME_PER_TIMECOST
        TIME_PER_TIMECOST = get_time_per_time_cost(16)
        print("TIME_PER_TIMECOST = ", TIME_PER_TIMECOST)
   
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
        # finds machine performance
        Thread(target=self.find_performance_argon).start()
        return sm

if __name__ == "__main__":  
    Config.set('graphics', 'width', '384')
    Config.set('graphics', 'height', '681')
    DerivatexApp().run()