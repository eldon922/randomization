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
            ErrorPopup().open("Nilai K lebih besar dari dimensi dataset!\nMohon mengganti nilai variabel Epsilon!")
            return False

        return True

    def browse_load_button_action(self):
        path = filedialog.askopenfilename(filetypes=[("Comma-separated Values", ".csv")])
        if path == "":
            return

        self.loading_popup = LoadingPopup()
        self.loading_popup.title = "Memuat Dokumen"
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
        self.dataset_description_layout.add_widget(DescriptionLabel("Nama Dokumen", self.csv_preprocessor.getFileName()))
        self.dataset_description_layout.add_widget(
            DescriptionLabel("Jumlah Baris", str(self.dataset.getNumberOfRows())))
        self.loading_popup.progress(80)
        self.dataset_description_layout.add_widget(
            DescriptionLabel("Jumlah Kolom", str(self.dataset.getNumberOfColumns())))
        self.k_label = DescriptionLabel("Nilai K", "Belum dihitung")
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
        if self.load_file_path.text == "Belum ada dokumen CSV yang dipilih untuk dirandomisasi":
            ErrorPopup().open("Mohon memilih dataset(dokumen CSV) terlebih dahulu!")
            return True
        else:
            return False

    def save_file_path_empty(self):
        if self.save_file_path.text == "Belum ada direktori yang dipilih untuk menyimpan hasil randomisasi":
            ErrorPopup().open("Mohon memilih direktori untuk menyimpan hasil randomisasi terlebih dahulu!")
            return True
        else:
            return False

    def epsilon_not_valid(self):
        if self.epsilon_value.text == "":
            ErrorPopup().open("Mohon menentukan nilai variabel Epsilon terlebih dahulu!")
            return True

        try:
            float(self.epsilon_value.text)
        except ValueError:
            ErrorPopup().open("Anda tidak memasukan nilai(bilangan desimal) dengan benar untuk variabel Epsilon!\nMohon periksa kembali dengan teliti!")
            return True

        if not 1 > float(self.epsilon_value.text) > 0:
            ErrorPopup().open("Nilai variabel Epsilon wajib berada pada rentang nilai lebih dari 0 dan kurang dari 1!")
            return True

        return False

    def dimension_target_not_valid(self):
        if self.dimension_value.text == "":
            ErrorPopup().open("Mohon menentukan target dimensi terlebih dahulu!")
            return True

        try:
            int(self.dimension_value.text)
        except ValueError:
            ErrorPopup().open("Anda tidak memasukan nilai(bilangan bulat) dengan benar untuk target dimensi!\nMohon periksa kembali dengan teliti!")
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

        if self.technique_spinner.text == "Random Rotation Perturbation":
            randomizer = RandomRotationPerturbation(self.dataset)
            self.loading_popup.progress(50)
            try:
                randomizer.perturbDataset()
            except TypeError:
                self.loading_popup.dismiss()
                ErrorPopup().open(
                    "Ada nilai yang tidak bersifat numerik pada dataset! Semua nilai harus berupa numerik!")
                return
            self.loading_popup.progress(80)
        else:
            randomizer = RandomProjectionPerturbation(self.dataset, float(self.epsilon_value.text),
                                                      int(self.dimension_value.text))

            if not self.calculate_and_check_k(randomizer):
                self.loading_popup.dismiss()
                return

            if not randomizer.checkDimensionTarget():
                self.loading_popup.dismiss()
                ErrorPopup().open(
                    "Nilai dari target dimensi wajib berada pada rentang nilai lebih besar dari atau sama dengan K "
                    "dan lebih kecil dari atau sama dengan dimensi dataset yang ingin dirandomisasi! Configure the "
                    "dimension target!")
                return
            self.loading_popup.progress(50)
            try:
                randomizer.perturbDataset()
            except TypeError:
                self.loading_popup.dismiss()
                ErrorPopup().open(
                    "Ada nilai yang tidak bersifat numerik pada dataset! Semua nilai harus berupa numerik!")
                return
            self.loading_popup.progress(80)

        if self.csv_preprocessor.matrixToCSV(randomizer.getPerturbedDataset(), self.save_file_path.text):
            self.loading_popup.dismiss()
            ErrorPopup().open(
                "Sudah ada file yang bernama " + self.csv_preprocessor.getResultFileName() + " pada direktori yang "
                                                                                             "dipilih!\nMohon dihapus "
                                                                                             "terlebih dahulu!")
            return

        self.randomization_result_description_layout.clear_widgets()
        self.randomization_result_description_layout.add_widget(
            DescriptionLabel("Nama File", self.csv_preprocessor.getResultFileName()))
        self.randomization_result_description_layout.add_widget(
            DescriptionLabel("Jumlah Kolom", str(randomizer.getPerturbedDataset().getNumberOfColumns())))
        if self.technique_spinner.text == "Random Projection Perturbation":
            self.randomization_result_description_layout.add_widget(
                DescriptionLabel("Nilai variabel epsilon yang dipakai", str(randomizer.getEpsilon())))
            self.randomization_result_description_layout.add_widget(
                DescriptionLabel("nilai K yang dipakai", str(randomizer.getK())))
        self.randomization_result_description_layout.add_widget(Label())

        self.loading_popup.progress(100)
        self.loading_popup.dismiss()
        ErrorPopup().open(self.technique_spinner.text + " berhasil diterapkan pada dataset yang dipilih!")


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
