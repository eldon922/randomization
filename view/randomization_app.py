from kivy.config import Config
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '600')
Config.set('kivy', 'window_icon', 'view/assets/r.ico')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.core.window import Window
# Window.clearcolor = (214/255.0, 217/255.0, 223/255.0, 1)
Window.clearcolor = (1, 1, 1, 1)
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.app import App
from kivy.uix.button import Button

from .main_menu import MainMenu
class HoverBehavior(object):
    """Hover behavior.
    :Events:
        `on_enter`
            Fired when mouse enter the bbox of the widget.
        `on_leave`
            Fired when the mouse exit the widget
    """

    hovered = BooleanProperty(False)
    border_point= ObjectProperty(None)
    '''Contains the last relevant point received by the Hoverable. This can
    be used in `on_enter` or `on_leave` in order to know where was dispatched the event.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        #Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            #We have already done what was needed
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        pass

    def on_leave(self):
        pass

from kivy.factory import Factory
Factory.register('HoverBehavior', HoverBehavior)

class HoverButton(Button, HoverBehavior):
    def on_enter(self, *args):
        Window.set_system_cursor("hand")
        self.background_color = 1,1,1,1

    def on_leave(self, *args):
        Window.set_system_cursor("arrow")
        self.background_color = 0,0,0,0

class HoverSpinner(Spinner, HoverBehavior):
    def on_enter(self, *args):
        Window.set_system_cursor("hand")

    def on_leave(self, *args):
        Window.set_system_cursor("arrow")

class HoverTextInput(TextInput, HoverBehavior):
    def on_enter(self, *args):
        Window.set_system_cursor("ibeam")

    def on_leave(self, *args):
        Window.set_system_cursor("arrow")

class RandomizationApp(App):
    def build(self):
        return MainMenu()