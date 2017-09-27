__all__ = ('Settings', 'SettingsPanel', 'SettingItem', 'SettingString',
           'SettingPath', 'SettingBoolean', 'SettingNumeric', 'SettingOptions',
           'SettingTitle', 'SettingsWithSidebar', 'SettingsWithSpinner',
           'SettingsWithTabbedPanel', 'SettingsWithNoMenu',
           'InterfaceWithSidebar', 'ContentPanel', 'MenuSidebar','SettingButtons'
           ,'SettingDatePicker')

import json
import os
from kivy.factory import Factory
from kivy.metrics import dp
from kivy.config import ConfigParser
from kivy.animation import Animation
from kivy.compat import string_types, text_type
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, ListProperty, \
    BooleanProperty, NumericProperty, DictProperty, ReferenceListProperty

from calendar_widget import *

class SettingSpacer(Widget):
    pass

class SettingItem(FloatLayout):
    title = StringProperty('<No title set>')
    desc = StringProperty(None, allownone=True)
    disabled = BooleanProperty(False)
    section = StringProperty(None)
    key = StringProperty(None)
    value = ObjectProperty(None)
    panel = ObjectProperty(None)
    content = ObjectProperty(None)
    selected_alpha = NumericProperty(0)

    __events__ = ('on_release', )

    def __init__(self, **kwargs):
        super(SettingItem, self).__init__(**kwargs)
        self.value = self.panel.get_value(self.section, self.key)

    def add_widget(self, *largs):
        if self.content is None:
            return super(SettingItem, self).add_widget(*largs)
        return self.content.add_widget(*largs)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if self.disabled:
            return
        touch.grab(self)
        self.selected_alpha = 1
        return super(SettingItem, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.dispatch('on_release')
            Animation(selected_alpha=0, d=.25, t='out_quad').start(self)
            return True
        return super(SettingItem, self).on_touch_up(touch)

    def on_release(self):
        pass

    def on_value(self, instance, value):
        if not self.section or not self.key:
            return
        # get current value in config
        panel = self.panel
        if not isinstance(value, string_types):
            value = str(value)
        panel.set_value(self.section, self.key, value)

class SettingDatePicker(SettingItem):
    pHint_x = NumericProperty(0.7)
    pHint_y = NumericProperty(0.7)
    pHint = ReferenceListProperty(pHint_x ,pHint_y)
    def __init__(self,touch_switch=False, *args,**kwargs):
        self.register_event_type('on_release')
        self.touch_switch = touch_switch
        super(SettingItem, self).__init__(*args,**kwargs)
        for aButton in kwargs["buttons"]:
            oButton=Button(text=aButton['title'], font_size= '15sp')
            oButton.ID=aButton['id']
            oButton.bind (on_release=self.run)
            self.add_widget(oButton)
            
    
    def set_value(self, section, key, value):
        # set_value normally reads the configparser values and runs on an error
        # to do nothing here
        return

    def show_popup(self, isnt, val):
        self.popup.size_hint=self.pHint        
        if val:
            Window.release_all_keyboards()
            self.popup.open()
        
    def update_value(self,instance):
        instance.text = "%s-%s-%s" % tuple(self.cal.active_date)
        self.panel.settings.dispatch('on_config_change',self.panel.config, self.section, self.key, instance.text)
        self.focus = False

    def run(self,instance):
        instance.text= today_date()
        self.cal = CalendarWidget(as_popup=True, touch_switch=self.touch_switch)
        self.popup = Popup(content=self.cal, on_dismiss=lambda x:self.update_value(instance), title="Calendar")
        self.cal.parent_popup = self.popup
        self.show_popup(instance,today_date())
        


class SettingButtons(SettingItem):
    def __init__(self, **kwargs):
        self.register_event_type('on_release')
        super(SettingItem, self).__init__(**kwargs)
        for aButton in kwargs["buttons"]:
            oButton=Button(text=aButton['title'], font_size= '15sp')
            oButton.ID=aButton['id']
            self.add_widget(oButton)
            oButton.bind (on_release=self.On_ButtonPressed)
    def set_value(self, section, key, value):
        # set_value normally reads the configparser values and runs on an error
        # to do nothing here
        return
    def On_ButtonPressed(self,instance):
        self.panel.settings.dispatch('on_config_change',self.panel.config, self.section, self.key, instance.ID)


class SettingBoolean(SettingItem):
    values = ListProperty(['0', '1'])

class SettingString(SettingItem):
    popup = ObjectProperty(None, allownone=True)
    textinput = ObjectProperty(None)

    def on_panel(self, instance, value):
        if value is None:
            return
        self.fbind('on_release', self._create_popup)

    def _dismiss(self, *largs):
        if self.textinput:
            self.textinput.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None

    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.text.strip()
        self.value = value

    def _create_popup(self, instance):
        # create popup layout
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            title=self.title, content=content, size_hint=(None, None),
            size=(popup_width, '250dp'))

        # create the textinput used for numeric input
        self.textinput = textinput = TextInput(
            text=self.value, font_size='24sp', multiline=False,
            size_hint_y=None, height='42sp')
        textinput.bind(on_text_validate=self._validate)
        self.textinput = textinput

        # construct the content, widget are used as a spacer
        content.add_widget(Widget())
        content.add_widget(textinput)
        content.add_widget(Widget())
        content.add_widget(SettingSpacer())

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        btn = Button(text='Ok')
        btn.bind(on_release=self._validate)
        btnlayout.add_widget(btn)
        btn = Button(text='Cancel')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()

class SettingPath(SettingItem):
    popup = ObjectProperty(None, allownone=True)
    textinput = ObjectProperty(None)
    show_hidden = BooleanProperty(False)
    dirselect = BooleanProperty(True)

    def on_panel(self, instance, value):
        if value is None:
            return
        self.fbind('on_release', self._create_popup)

    def _dismiss(self, *largs):
        if self.textinput:
            self.textinput.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None

    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.selection

        if not value:
            return

        self.value = os.path.realpath(value[0])

    def _create_popup(self, instance):
        # create popup layout
        content = BoxLayout(orientation='vertical', spacing=5)
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            title=self.title, content=content, size_hint=(None, 0.9),
            width=popup_width)

        # create the filechooser
        initial_path = self.value or os.getcwd()
        self.textinput = textinput = FileChooserListView(
            path=initial_path, size_hint=(1, 1),
            dirselect=self.dirselect, show_hidden=self.show_hidden)
        textinput.bind(on_path=self._validate)

        # construct the content
        content.add_widget(textinput)
        content.add_widget(SettingSpacer())

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        btn = Button(text='Ok')
        btn.bind(on_release=self._validate)
        btnlayout.add_widget(btn)
        btn = Button(text='Cancel')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()

class SettingNumeric(SettingString):

    def _validate(self, instance):
        is_float = '.' in str(self.value)
        self._dismiss()
        try:
            if is_float:
                self.value = text_type(float(self.textinput.text))
            else:
                self.value = text_type(int(self.textinput.text))
        except ValueError:
            return

class SettingOptions(SettingItem):
    options = ListProperty([])
    popup = ObjectProperty(None, allownone=True)

    def on_panel(self, instance, value):
        if value is None:
            return
        self.fbind('on_release', self._create_popup)

    def _set_option(self, instance):
        self.value = instance.text
        self.popup.dismiss()

    def _create_popup(self, instance):
        # create the popup
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            content=content, title=self.title, size_hint=(None, None),
            size=(popup_width, '400dp'))
        popup.height = len(self.options) * dp(55) + dp(150)

        # add all the options
        content.add_widget(Widget(size_hint_y=None, height=1))
        uid = str(self.uid)
        for option in self.options:
            state = 'down' if option == self.value else 'normal'
            btn = ToggleButton(text=option, state=state, group=uid)
            btn.bind(on_release=self._set_option)
            content.add_widget(btn)

        # finally, add a cancel button to return on the previous panel
        content.add_widget(SettingSpacer())
        btn = Button(text='Cancel', size_hint_y=None, height=dp(50))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)

        # and open the popup !
        popup.open()

class SettingTitle(Label):
    title = Label.text
    panel = ObjectProperty(None)

class SettingsPanel(GridLayout):
    title = StringProperty('Default title')
    config = ObjectProperty(None, allownone=True)
    settings = ObjectProperty(None)

    def __init__(self, **kwargs):
        if 'cols' not in kwargs:
            self.cols = 1
        super(SettingsPanel, self).__init__(**kwargs)

    def on_config(self, instance, value):
        if value is None:
            return
        if not isinstance(value, ConfigParser):
            raise Exception('Invalid config object, you must use a'
                            'kivy.config.ConfigParser, not another one !')

    def get_value(self, section, key):
        config = self.config
        if not config:
            return
        return config.get(section, key)


    def set_value(self, section, key, value):
        current = self.get_value(section, key)
        if current == value:
            return
        config = self.config
        if config:
            config.set(section, key, value)
            config.write()
        settings = self.settings
        if settings:
            settings.dispatch('on_config_change',
                              config, section, key, value)


class InterfaceWithSidebar(BoxLayout):
    menu = ObjectProperty()
    content = ObjectProperty()
    __events__ = ('on_close', )

    def __init__(self, *args, **kwargs):
        super(InterfaceWithSidebar, self).__init__(*args, **kwargs)
        self.menu.close_button.bind(
            on_release=lambda j: self.dispatch('on_close'))

    def add_panel(self, panel, name, uid):
        self.menu.add_item(name, uid)
        self.content.add_panel(panel, name, uid)

    def on_close(self, *args):
        pass

class ContentPanel(ScrollView):
    panels = DictProperty({})
    container = ObjectProperty()
    current_panel = ObjectProperty(None)
    current_uid = NumericProperty(0)

    def add_panel(self, panel, name, uid):
        self.panels[uid] = panel
        if not self.current_uid:
            self.current_uid = uid

    def on_current_uid(self, *args):
        uid = self.current_uid
        if uid in self.panels:
            if self.current_panel is not None:
                self.remove_widget(self.current_panel)
            new_panel = self.panels[uid]
            self.add_widget(new_panel)
            self.current_panel = new_panel
            return True
        return False  # New uid doesn't exist

    def add_widget(self, widget):
        if self.container is None:
            super(ContentPanel, self).add_widget(widget)
        else:
            self.container.add_widget(widget)

    def remove_widget(self, widget):
        self.container.remove_widget(widget)

class Settings(BoxLayout):
    interface = ObjectProperty(None)
    interface_cls = ObjectProperty(InterfaceWithSidebar)
    __events__ = ('on_close', 'on_config_change')

    def __init__(self, *args, **kargs):
        self._types = {}
        super(Settings, self).__init__(*args, **kargs)
        self.add_interface()
        self.register_type('string', SettingString)
        self.register_type('bool', SettingBoolean)
        self.register_type('numeric', SettingNumeric)
        self.register_type('options', SettingOptions)
        self.register_type('title', SettingTitle)
        self.register_type('path', SettingPath)
        self.register_type('buttons', SettingButtons)
        self.register_type('datePicker', SettingDatePicker)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            super(Settings, self).on_touch_down(touch)
            return True

    def register_type(self, tp, cls):
        self._types[tp] = cls

    def on_close(self, *args):
        pass

    def add_interface(self):
        cls = self.interface_cls
        if isinstance(cls, string_types):
            cls = Factory.get(cls)
        interface = cls()
        self.interface = interface
        self.add_widget(interface)
        self.interface.bind(on_close=lambda j: self.dispatch('on_close'))

    def on_config_change(self, config, section, key, value):
        pass

    def add_json_panel(self, title, config, filename=None, data=None):
        panel = self.create_json_panel(title, config, filename, data)
        uid = panel.uid
        if self.interface is not None:
            self.interface.add_panel(panel, title, uid)

    def create_json_panel(self, title, config, filename=None, data=None):
        
        if filename is None and data is None:
            raise Exception('You must specify either the filename or data')
        if filename is not None:
            with open(filename, 'r') as fd:
                data = json.loads(fd.read())
        else:
            data = json.loads(data)
        if type(data) != list:
            raise ValueError('The first element must be a list')
        panel = SettingsPanel(title=title, settings=self, config=config)

        for setting in data:
            # determine the type and the class to use
            if 'type' not in setting:
                raise ValueError('One setting are missing the "type" element')
            ttype = setting['type']
            cls = self._types.get(ttype)
            if cls is None:
                raise ValueError(
                    'No class registered to handle the <%s> type' %
                    setting['type'])

            # create a instance of the class, without the type attribute
            del setting['type']
            str_settings = {}
            for key, item in setting.items():
                str_settings[str(key)] = item

            instance = cls(panel=panel, **str_settings)

            # instance created, add to the panel
            panel.add_widget(instance)

        return panel


    def add_kivy_panel(self):
        from kivy import kivy_data_dir
        from kivy.config import Config
        from os.path import join

        import os
        Config.setdefaults('app', {
            'bool': True,
            'numeric': 10,
            'options': 'option2',
            'string': 'some_string',
            'path': '/some/path'})

        self.add_json_panel('Retrofit', Config,
            join(os.getcwd(), 'retrofit.json'))
        self.add_json_panel('Unretrofit', Config,
            join(os.getcwd(), 'retrofit.json'))
        self.add_json_panel('Lean Analysis', Config,
            join(os.getcwd(), 'retrofit.json'))

class SettingsWithSidebar(Settings):
    pass

class MenuSidebar(FloatLayout):
    selected_uid = NumericProperty(0)
    buttons_layout = ObjectProperty(None)
    close_button = ObjectProperty(None)

    def add_item(self, name, uid):
        label = SettingSidebarLabel(text=name, uid=uid, menu=self)
        if len(self.buttons_layout.children) == 0:
            label.selected = True
        if self.buttons_layout is not None:
            self.buttons_layout.add_widget(label)

    def on_selected_uid(self, *args):
        for button in self.buttons_layout.children:
            if button.uid != self.selected_uid:
                button.selected = False

class SettingSidebarLabel(Label):
    # Internal class, not documented.
    selected = BooleanProperty(False)
    uid = NumericProperty(0)
    menu = ObjectProperty(None)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        self.selected = True
        self.menu.selected_uid = self.uid

# if __name__ == '__main__':
#     from kivy.app import App

#     class SettingsApp(App):

#         def build(self):
#             s = Settings()
#             s.add_kivy_panel()
#             s.bind(on_close=self.stop)
#             s.bind(on_config_change=self.On_config_change)
#             return s

#         def On_config_change(self, settings, config, section, key, value):
#             print key
#             if section==u'MyApp':
#                 if key==u'button_run':
#                     print ("run pressed")

#     SettingsApp().run()