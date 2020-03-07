from tkinter import Tk, filedialog

from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout


class BrowseFile(GridLayout):
    file_path = ObjectProperty(None)

    def browse(self):
        root = Tk()
        root.withdraw()

        path = filedialog.askopenfilename(filetypes=[("Comma-separated Values", ".csv")])

        self.file_path.text = path
