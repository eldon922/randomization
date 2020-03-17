from threading import Thread
from tkinter import Tk, filedialog

from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from perturbation.random_projection_perturbation import RandomProjectionPerturbation
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
    calculate_k_button = ObjectProperty(None)

    technique_spinner = ObjectProperty(None)

    dataset_description_layout = ObjectProperty(None)
    randomization_result_description_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_technique_spinner_select("Random Rotation Perturbation")

    def calculate_k_button_action(self):
        if self.load_file_path_empty() or self.epsilon_not_valid():
            return

        randomizer = RandomProjectionPerturbation(self.dataset, float(self.epsilon_value.text))

        self.calculate_and_check_k(randomizer)

    def calculate_and_check_k(self, randomizer):
        self.k_label.change_value(str(randomizer.getK()))

        if not randomizer.checkK():
            ErrorPopup().open("K value is bigger than the dimension of dataset! Configure the epsilon variable!")
            return False

        return True

    def browse_load_button_action(self):
        path = filedialog.askopenfilename(filetypes=[("Comma-separated Values", ".csv")])
        if path == "":
            return

        self.loading_popup = LoadingPopup()
        self.loading_popup.title = "Load File"
        self.loading_popup.open()
        self.loading_popup.progress(40)

        self.load_file_path.text = path

        load_file_thread = Thread(target=self.browse_load)
        load_file_thread.start()

    def browse_load(self):
        self.csv_preprocessor = CSVPreprocessor()
        self.csv_preprocessor.readCSV(self.load_file_path.text)
        self.dataset = self.csv_preprocessor.csvToMatrix()

        self.dataset_description_layout.clear_widgets()

        self.loading_popup.progress(60)
        self.dataset_description_layout.add_widget(DescriptionLabel("File Name", self.csv_preprocessor.getFileName()))
        self.dataset_description_layout.add_widget(
            DescriptionLabel("Number of Rows", str(self.dataset.getNumberOfRows())))
        self.loading_popup.progress(80)
        self.dataset_description_layout.add_widget(
            DescriptionLabel("Number of Columns", str(self.dataset.getNumberOfColumns())))
        self.k_label = DescriptionLabel("K Value", "Not calculated yet.")
        self.dataset_description_layout.add_widget(self.k_label)
        if self.technique_spinner.text == "Random Rotation Perturbation":
            hide_widget(self.k_label)
        self.dataset_description_layout.add_widget(Label())
        self.loading_popup.progress(100)
        self.loading_popup.dismiss()

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
            try:
                hide_widget(self.k_label)
            except AttributeError:
                pass
            hide_widget(self.calculate_k_button)
        else:
            hide_widget(self.dimension_label, False)
            hide_widget(self.dimension_value, False)
            hide_widget(self.epsilon_label, False)
            hide_widget(self.epsilon_value, False)
            try:
                hide_widget(self.k_label, False)
            except AttributeError:
                pass
            hide_widget(self.calculate_k_button, False)

    def load_file_path_empty(self):
        if self.load_file_path.text == 'No file selected':
            ErrorPopup().open("Please select dataset file first!")
            return True
        else:
            return False

    def save_file_path_empty(self):
        if self.save_file_path.text == 'No folder selected':
            ErrorPopup().open("Please select folder path for save the result first!")
            return True
        else:
            return False

    def epsilon_not_valid(self):
        if self.epsilon_value.text == "":
            ErrorPopup().open("Please decide epsilon variable first!")
            return True

        try:
            float(self.epsilon_value.text)
        except ValueError:
            ErrorPopup().open("You don't fill appropriate number for epsilon variable!")
            return True

        if not 1 > float(self.epsilon_value.text) > 0:
            ErrorPopup().open("Epsilon variable need to be in range from 0 and 1, inclusively!")
            return True

        return False

    def dimension_target_not_valid(self):
        if self.dimension_value.text == "":
            ErrorPopup().open("Please decide dimension target first!")
            return True

        try:
            int(self.dimension_value.text)
        except ValueError:
            ErrorPopup().open("You don't fill appropriate number for dimension target!")
            return True

        return False

    def randomize_button_action(self):
        if self.load_file_path_empty() or self.save_file_path_empty():
            return
        if self.technique_spinner.text == "Random Projection Perturbation" and (self.epsilon_not_valid()
                                                                                or self.dimension_target_not_valid()):
            return

        self.loading_popup = LoadingPopup()
        self.loading_popup.title = self.technique_spinner.text
        self.loading_popup.open()

        self.loading_popup.progress(10)

        randomize_thread = Thread(target=self.randomize)
        randomize_thread.start()

    def randomize(self):
        self.loading_popup.progress(30)

        if self.technique_spinner.text == "Random Projection Perturbation":
            randomizer = RandomRotationPerturbation(self.dataset)
            randomizer = RandomProjectionPerturbation(self.dataset, float(self.epsilon_value.text),
                                                      int(self.dimension_value.text))

            if not self.calculate_and_check_k(randomizer):
                self.loading_popup.dismiss()
                return

            if not randomizer.checkDimensionTarget():
                self.loading_popup.dismiss()
                ErrorPopup().open(
                    "Dimension target must be more equal than K and less equal than the dimension of dataset! "
                    "Configure the dimension target!")
                return
            self.loading_popup.progress(50)
            try:
                randomizer.perturbDataset()
            except TypeError:
                self.loading_popup.dismiss()
                ErrorPopup().open(
                    "There is non-numeric value in the dataset! It's must be numeric!")
                return
            self.loading_popup.progress(80)
            print("randomize projection!")
        else:
            randomizer = RandomRotationPerturbation(self.dataset)
            self.loading_popup.progress(50)
            try:
                randomizer.perturbDataset()
            except TypeError:
                self.loading_popup.dismiss()
                ErrorPopup().open(
                    "There is non-numeric value in the dataset! It's must be numeric!")
                return
            self.loading_popup.progress(80)

        if self.csv_preprocessor.matrixToCSV(randomizer.getPerturbedDataset(), self.save_file_path.text):
            self.loading_popup.dismiss()
            ErrorPopup().open(
                "You already have file with name " + self.csv_preprocessor.getResultFileName() + "! Please delete it.")
            return

        self.randomization_result_description_layout.clear_widgets()
        self.randomization_result_description_layout.add_widget(
            DescriptionLabel("File Name", self.csv_preprocessor.getResultFileName()))
        self.randomization_result_description_layout.add_widget(
            DescriptionLabel("Number of Columns", str(randomizer.getPerturbedDataset().getNumberOfColumns())))
        if self.technique_spinner.text == "Random Projection Perturbation":
            self.randomization_result_description_layout.add_widget(
                DescriptionLabel("Using Epsilon Value", str(randomizer.getEpsilon())))
            self.randomization_result_description_layout.add_widget(
                DescriptionLabel("Using K Value", str(randomizer.getK())))
        self.randomization_result_description_layout.add_widget(Label())

        self.loading_popup.progress(100)
        self.loading_popup.dismiss()
        ErrorPopup().open(self.technique_spinner.text + " has been successfully applied to dataset!")


class ErrorPopup(Popup):
    text_label = ObjectProperty(None)

    def open(self, text, *largs, **kwargs):
        self.text_label.text = text
        super().open()


class LoadingPopup(Popup):
    progress_bar = ObjectProperty(None)
    progress_label = ObjectProperty(None)

    def progress(self, value):
        self.progress_bar.value = value
        self.progress_label.text = str(value) + "%"


class DescriptionLabel(Label):
    def __init__(self, title, value):
        self.title = title
        super().__init__(text=title + ": " + value)

    def change_value(self, value):
        self.text = self.title + ": " + value
