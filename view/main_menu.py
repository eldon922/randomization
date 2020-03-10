from tkinter import Tk, filedialog

from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from perturbation.random_rotation_perturbation import RandomRotationPerturbation
from preprocessor.csv_preprocessor import CSVPreprocessor

root = Tk()
root.iconbitmap('view/assets/r.ico')
root.withdraw()


def hide_widget(wid, do_hide=True):
    if hasattr(wid, 'saved_attrs'):
        if not do_hide:
            wid.height, wid.size_hint_y, wid.opacity, wid.disabled = wid.saved_attrs
            del wid.saved_attrs
    elif do_hide:
        wid.saved_attrs = wid.height, wid.size_hint_y, wid.opacity, wid.disabled
        wid.height, wid.size_hint_y, wid.opacity, wid.disabled = 0, None, 0, True


class MainMenu(GridLayout):
    load_file_path = ObjectProperty(None)
    save_file_path = ObjectProperty(None)

    dimension_label = ObjectProperty(None)
    dimension_value = ObjectProperty(None)
    epsilon_label = ObjectProperty(None)
    epsilon_value = ObjectProperty(None)

    technique_spinner = ObjectProperty(None)

    def browse_load(self):
        path = filedialog.askopenfilename(filetypes=[("Comma-separated Values", ".csv")])

        if path != "":
            self.load_file_path.text = path

    def browse_save(self):
        path = filedialog.askdirectory()

        if path != "":
            self.save_file_path.text = path

    def on_technique_spinner_select(self, text):
        if text == "Random Rotation Perturbation":
            hide_widget(self.dimension_label)
            hide_widget(self.dimension_value)
            hide_widget(self.epsilon_label)
            hide_widget(self.epsilon_value)
        else:
            hide_widget(self.dimension_label, False)
            hide_widget(self.dimension_value, False)
            hide_widget(self.epsilon_label, False)
            hide_widget(self.epsilon_value, False)

    def randomize(self):
        if self.load_file_path.text == 'No file selected':
            LoadFilePopup().open()
            return
        elif self.save_file_path.text == 'No folder selected':
            LoadFilePopup().open(False)
            return

        csv_preprocessor = CSVPreprocessor()
        csv_preprocessor.readCSV(self.load_file_path.text)

        csv_preprocessor.dropColumn('subject')
        csv_preprocessor.dropColumn('Activity')

        dataset = csv_preprocessor.csvToMatrix()

        if self.technique_spinner.text == "Random Projection Perturbation":
            print("randomize projection!")
        else:
            rotation_randomizer = RandomRotationPerturbation(dataset)
            rotation_randomizer.perturbDataset()
            csv_preprocessor.matrixToCSV(rotation_randomizer.getPerturbedDataset(), self.save_file_path.text)
            print("randomize rotation!")


class LoadFilePopup(Popup):
    text_label = ObjectProperty(None)

    def open(self, load=True, *largs, **kwargs):
        if load:
            self.text_label.text = "Please select dataset file first!"
        else:
            self.text_label.text = "Please select folder path for save the result first!"
        super().open()

