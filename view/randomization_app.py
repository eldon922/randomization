from kivy.app import App
from .main_menu import MainMenu

from kivy.config import Config
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '600')
Config.set('kivy', 'window_icon', 'view/assets/r.ico')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class RandomizationApp(App):
    def build(self):
        return MainMenu()
