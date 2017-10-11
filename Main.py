import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics','show_cursor','1')
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingItem
from kivy.uix.button import Button
import os
from customSettings import Settings
from customSettings import SettingsWithSidebar
import json
from table import *


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(BoxLayout):
    sm=None
    def __init__(self, **kwargs):
        super(Root,self).__init__(**kwargs)
        

    def changeScreen(self, buttonTxt):
        if buttonTxt == "login":
            self.ids.screen_manager.current="main_screen"
        elif buttonTxt=="logout":
            self.ids.screen_manager.current="login_screen"
        Root.sm=self.ids.screen_manager

    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)
            self.dismiss_popup()

 
class MainApp(App):
    def build(self):
        self.settings_cls = SettingsWithSidebar
    	return Root()

    x=["Alpha","Bravo","Charley","Delta","Echo","Foxtrot","xray"]
    def populateList(lst):
        with open('retrofit.json') as data_file:    
            data = json.load(data_file)
        data[3]["options"]=lst
        with open('retrofit.json', 'w') as outfile:
            json.dump(data, outfile)
        return lst
    populateList(x)

    def build_settings(self,settings):
        settings.bind(on_close=self.stop)
        settings.bind(on_config_change=self.On_config_change)
        return settings

    def On_config_change(self, settings, config, section, key, value):
        if section==u'app':
            if key==u'button_run':
                super(MainApp, self).close_settings()
                Root.sm.current="query_screen"
                Grid()
            elif key==u'stndDate':
                if(value==u'start_Date'):
                    print "start date" ,value
                else:
                    print "end Date", value


Factory.register('Root', cls=Root)
Factory.register('SaveDialog', cls=SaveDialog)


if __name__ == '__main__':
    MainApp().run()
