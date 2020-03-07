from kivy.app import App
from .main_menu import MainMenu


class RandomizationApp(App):
    def build(self):
        return MainMenu()
