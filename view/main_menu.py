import pathlib
from threading import Thread

from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from plyer import filechooser

from matrix.random_projection_matrix import RandomProjectionMatrix
from matrix.random_rotation_matrix import RandomRotationMatrix
from matrix.random_translation_matrix import RandomTranslationMatrix
from perturbation.random_projection_perturbation import RandomProjectionPerturbation
from perturbation.random_rotation_perturbation import RandomRotationPerturbation
from preprocessor.csv_preprocessor import CSVPreprocessor
from preprocessor.projection_matrix_preprocessor import ProjectionMatrixPreprocessor
from preprocessor.rotation_matrix_preprocessor import RotationMatrixPreprocessor


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

    dimension_label = ObjectProperty(None)
    dimension_value = ObjectProperty(None)
    epsilon_label = ObjectProperty(None)
    epsilon_value = ObjectProperty(None)
    calculate_k_button = ObjectProperty(None)

    technique_spinner = ObjectProperty(None)

    dataset_description_layout = ObjectProperty(None)
    randomization_result_description_layout = ObjectProperty(None)

    load_matrix_path = ObjectProperty(None)

    # guide_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_technique_spinner_select("Random Rotation Perturbation")

    #         self.guide_label.text = '''1. Pilih dataset yang berupa dokumen CSV dengan menekan tombol "Pilih Dokumen CSV". Ada 2 persyaratan yang harus dipenuhi yaitu baris pertama pada dokumen adalah nama-nama setiap kolom dan nilai pada dataset semuanya wajib berjenis numerik
    # 2. Pilih teknik yang ingin digunakan dengan menekan tombol yang bertulisan nama teknik yang sekarang dipilih. Defaultnya adalah "Random Rotation Perturbation"
    # 3. Apabila teknik yang dipilih adalah "Random Projection Perturbation", lakukan langkah berikut dahulu.
    #     - Tentukan nilai Epsilon yang diinginkan
    #     - Tekan tombol "Hitung Nilai K" untuk menghitung nilai K pada dataset dengan Epsilon yang telah ditentukan
    #     - Tentukan target dimensi yang diinginkan
    # 4. Tekan tombol "Randomisasi dan Simpan"
    # 5. Pilih direktori penyimpanan yang diinginkan untuk menyimpan hasil randomisasi'''

    def calculate_k_button_action(self):
        if self.load_file_path_empty() or self.epsilon_not_valid():
            return

        randomizer = RandomProjectionPerturbation(self.dataset, float(self.epsilon_value.text))

        self.calculate_and_check_k(randomizer)

    def calculate_and_check_k(self, randomizer):
        self.k_label.change_value(str(randomizer.getK()))

        if not randomizer.checkK():
            WarningPopup().open("Nilai K lebih besar dari dimensi dataset!\nMohon mengganti nilai variabel Epsilon!")
            return False

        return True

    def browse_load_button_action(self):
        # self.path = filedialog.askopenfilename()
        self.path = filechooser.open_file(title="Pilih dataset berbentuk dokumen CSV..",
                                          filters=[("Comma-separated Values", "*.csv")])
        if len(self.path) == 0:
            return

        self.loading_popup = LoadingPopup()
        self.loading_popup.title = "Memuat Dokumen"
        self.loading_popup.open()
        self.loading_popup.progress(40)

        load_file_thread = Thread(target=self.browse_load)
        load_file_thread.start()

    def browse_load(self):
        self.csv_preprocessor = CSVPreprocessor()
        try:
            self.csv_preprocessor.readCSV(self.path[0])
        except:
            WarningPopup().open("Dokumen CSV yang dimasukkan tidak sesuai dengan persyaratan!")
            self.loading_popup.dismiss()
            return

        self.dataset = self.csv_preprocessor.csvToMatrix()

        self.randomization_result_description_layout.clear_widgets()
        self.load_file_path.text = self.path[0]
        self.load_matrix_path.text = "Pilih matriks yang dipakai"
        self.randomTranslationMatrix = None
        self.randomRotationMatrix = None
        self.randomProjectionMatrix = None

        self.dataset_description_layout.clear_widgets()

        self.loading_popup.progress(60)
        self.dataset_description_layout.add_widget(
            DescriptionLabel("Nama Dokumen", self.csv_preprocessor.getFileName()))
        self.dataset_description_layout.add_widget(
            DescriptionLabel("Jumlah Baris", str(self.dataset.getNumberOfRows())))
        self.loading_popup.progress(80)
        self.dataset_description_layout.add_widget(
            DescriptionLabel("Jumlah Kolom", str(self.dataset.getNumberOfColumns())))
        self.k_label = DescriptionLabel("Nilai K", "Belum dihitung")
        self.dataset_description_layout.add_widget(self.k_label)
        if self.technique_spinner.text == "Random Rotation Perturbation":
            hide_widget(self.k_label)
        self.loading_popup.progress(100)
        self.loading_popup.dismiss()

    def browse_save(self):
        path = filechooser.save_file(title="Simpan hasil berbentuk dokumen CSV..",
                                     filters=[("Comma-separated Values", "*.csv")])

        if len(path) != 0:
            if pathlib.Path(path[0]).suffix == ".csv":
                return path[0]
            else:
                return path[0] + ".csv"
        else:
            False

    def on_technique_spinner_select(self, text):
        self.randomization_result_description_layout.clear_widgets()
        self.load_matrix_path.text = "Pilih matriks yang dipakai"
        self.randomTranslationMatrix = None
        self.randomRotationMatrix = None
        self.randomProjectionMatrix = None
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
            WarningPopup().open("Mohon memilih dataset(dokumen CSV) terlebih dahulu!")
            return True
        else:
            return False

    def load_matrix_path_empty(self):
        if self.load_matrix_path.text == "Pilih matriks yang dipakai":
            WarningPopup().open("Mohon memilih matriks(dokumen CSV) terlebih dahulu!")
            return True
        else:
            return False

    def epsilon_not_valid(self):
        if self.epsilon_value.text == "":
            WarningPopup().open("Mohon menentukan nilai variabel Epsilon terlebih dahulu!")
            return True

        try:
            float(self.epsilon_value.text)
        except ValueError:
            WarningPopup().open(
                "Anda tidak memasukan nilai(bilangan desimal) dengan benar untuk variabel Epsilon!\nMohon periksa "
                "kembali dengan teliti!")
            return True

        if not 1 > float(self.epsilon_value.text) > 0:
            WarningPopup().open(
                "Nilai variabel Epsilon wajib berada pada rentang nilai lebih dari 0 dan kurang dari 1!")
            return True

        return False

    def dimension_target_not_valid(self):
        if self.dimension_value.text == "":
            WarningPopup().open("Mohon menentukan target dimensi terlebih dahulu!")
            return True

        try:
            int(self.dimension_value.text)
        except ValueError:
            WarningPopup().open(
                "Anda tidak memasukan nilai(bilangan bulat) dengan benar untuk target dimensi!\nMohon periksa kembali "
                "dengan teliti!")
            return True

        return False

    def create_save_matrix_button_action(self):
        if self.load_file_path_empty():
            return

        if self.technique_spinner.text == "Random Rotation Perturbation":
            matrix_path = self.browse_save()
            if not matrix_path:
                return
            self.randomRotationMatrix = RandomRotationMatrix.generate(self.dataset.getNumberOfColumns())
            self.randomTranslationMatrix = RandomTranslationMatrix.generate(self.dataset.getNumberOfColumns() + 1)

            if RotationMatrixPreprocessor.save_to_csv(matrix_path, self.randomRotationMatrix, self.randomTranslationMatrix):
                self.loading_popup.dismiss()
                WarningPopup().open(
                    "Tolong menutup dokumen yang dipilih yaitu " + matrix_path)
                self.randomization_result_description_layout.add_widget(DescriptionLabel("Status", "GAGAL"))
                self.randomization_result_description_layout.add_widget(DescriptionLabel("Alasan",
                                                                                         "Sudah ada dokumen yang mempunyai nama yang sama yaitu " + matrix_path + " dan dibuka oleh program lain!\nMohon ditutup "
                                                                                                                                                                  "terlebih dahulu!"))
                return
        else:
            if self.epsilon_not_valid() or self.dimension_target_not_valid():
                # self.loading_popup.dismiss()
                return

            randomizer = RandomProjectionPerturbation(self.dataset, float(self.epsilon_value.text),
                                                      int(self.dimension_value.text))

            if not self.calculate_and_check_k(randomizer):
                # self.loading_popup.dismiss()
                return

            if not randomizer.checkDimensionTarget():
                # self.loading_popup.dismiss()
                WarningPopup().open(
                    "Nilai dari target dimensi wajib berada pada rentang nilai lebih besar dari atau sama dengan K "
                    "dan lebih kecil dari atau sama dengan dimensi dataset yang ingin dirandomisasi!\nMohon mengganti "
                    "target dimensi!")
                return
            self.randomProjectionMatrix = RandomProjectionMatrix.generate(self.dataset.getNumberOfColumns(),
                                                                          int(self.dimension_value.text),
                                                                          float(self.epsilon_value.text))

            matrix_path = self.browse_save()
            if not matrix_path:
                return

            if ProjectionMatrixPreprocessor.save_to_csv(matrix_path, self.randomProjectionMatrix):
                self.loading_popup.dismiss()
                WarningPopup().open(
                    "Tolong menutup dokumen yang dipilih yaitu " + matrix_path)
                self.randomization_result_description_layout.add_widget(DescriptionLabel("Status", "GAGAL"))
                self.randomization_result_description_layout.add_widget(DescriptionLabel("Alasan",
                                                                                         "Sudah ada dokumen yang mempunyai nama yang sama yaitu " + matrix_path + " dan dibuka oleh program lain!\nMohon ditutup "
                                                                                                                                                                "terlebih dahulu!"))
                return

        self.load_matrix_path.text = matrix_path

    def import_matrix_button_action(self):
        if self.load_file_path_empty():
            return

        matrix_path = filechooser.open_file(title="Pilih matriks berbentuk dokumen CSV..",
                                            filters=[("Comma-separated Values", "*.csv")])

        if len(matrix_path) == 0:
            return

        if self.technique_spinner.text == "Random Rotation Perturbation":
            try:
                rotationMatrixPreprocessor = RotationMatrixPreprocessor()
                if not rotationMatrixPreprocessor.read_from_csv(matrix_path[0], self.dataset.getNumberOfColumns()):
                    WarningPopup().open(
                        "Matriks yang dipilih tidak sesuai dengan dataset!")
                    return

                self.randomTranslationMatrix = rotationMatrixPreprocessor.getRandomTranslationMatrix()
                self.randomRotationMatrix = rotationMatrixPreprocessor.getRandomRotationMatrix()
            except:
                WarningPopup().open("Dokumen CSV yang dimasukkan tidak sesuai dengan persyaratan!")
                # self.loading_popup.dismiss()
                return
        else:
            projectionMatrixPreprocessor = ProjectionMatrixPreprocessor()
            if not projectionMatrixPreprocessor.read_from_csv(matrix_path[0], self.dataset.getNumberOfColumns()):
                WarningPopup().open(
                    "Matriks yang dipilih tidak sesuai dengan dataset!")
                return

            self.randomProjectionMatrix = projectionMatrixPreprocessor.getProjectionMatrix()
            self.dimension_value.text = str(self.randomProjectionMatrix.getNumberOfRows())

        self.load_matrix_path.text = matrix_path[0]

    def randomize_button_action(self):
        self.randomization_result_description_layout.clear_widgets()

        if self.load_file_path_empty() or self.load_matrix_path_empty():
            return

        if self.technique_spinner.text == "Random Projection Perturbation":
            if self.epsilon_not_valid() or self.dimension_target_not_valid():
                return
            elif self.randomProjectionMatrix.getNumberOfRows() != int(self.dimension_value.text):
                WarningPopup().open("Dimensi matriks tidak sama dengan dimensi target yang diinginkan!")
                return

        self.loading_popup = LoadingPopup()
        self.loading_popup.title = self.technique_spinner.text
        self.loading_popup.open()

        self.loading_popup.progress(10)

        randomize_thread = Thread(target=self.randomize)
        randomize_thread.start()

    def randomize(self):
        try:
            self.loading_popup.progress(30)

            if self.technique_spinner.text == "Random Rotation Perturbation":
                randomizer = RandomRotationPerturbation(self.dataset, self.randomTranslationMatrix,
                                                        self.randomRotationMatrix)
                self.loading_popup.progress(50)
                try:
                    randomizer.perturbDataset()
                except TypeError:
                    self.loading_popup.dismiss()
                    WarningPopup().open(
                        "Ada nilai yang tidak bersifat numerik pada dataset! Semua nilai harus berupa numerik!")
                    self.randomization_result_description_layout.add_widget(DescriptionLabel("Status", "GAGAL"))
                    self.randomization_result_description_layout.add_widget(DescriptionLabel("Alasan",
                                                                                             "Ada nilai yang tidak "
                                                                                             "bersifat numerik pada "
                                                                                             "dataset! Semua nilai harus "
                                                                                             "berupa numerik!"))
                    return
            else:
                randomizer = RandomProjectionPerturbation(self.dataset, float(self.epsilon_value.text),
                                                          int(self.dimension_value.text), self.randomProjectionMatrix)

                if not self.calculate_and_check_k(randomizer):
                    self.loading_popup.dismiss()
                    return

                if not randomizer.checkDimensionTarget():
                    self.loading_popup.dismiss()
                    WarningPopup().open(
                        "Nilai dari target dimensi wajib berada pada rentang nilai lebih besar dari atau sama dengan K "
                        "dan lebih kecil dari atau sama dengan dimensi dataset yang ingin dirandomisasi!\nMohon mengganti "
                        "target dimensi!")
                    self.randomization_result_description_layout.add_widget(DescriptionLabel("Status", "GAGAL"))
                    self.randomization_result_description_layout.add_widget(DescriptionLabel("Alasan",
                                                                                             "Nilai dari target dimensi "
                                                                                             "wajib berada pada rentang "
                                                                                             "nilai lebih besar dari atau "
                                                                                             "sama dengan K "
                                                                                             "dan lebih kecil dari atau "
                                                                                             "sama dengan dimensi dataset "
                                                                                             "yang ingin "
                                                                                             "dirandomisasi!\nMohon "
                                                                                             "mengganti "
                                                                                             "target dimensi!"))
                    return
                self.loading_popup.progress(50)
                try:
                    randomizer.perturbDataset()
                except TypeError:
                    self.loading_popup.dismiss()
                    WarningPopup().open(
                        "Ada nilai yang tidak bersifat numerik pada dataset! Semua nilai harus berupa numerik!")
                    self.randomization_result_description_layout.add_widget(DescriptionLabel("Status", "GAGAL"))
                    self.randomization_result_description_layout.add_widget(DescriptionLabel("Alasan", "Ada nilai yang "
                                                                                                       "tidak bersifat "
                                                                                                       "numerik pada "
                                                                                                       "dataset! Semua "
                                                                                                       "nilai harus "
                                                                                                       "berupa numerik!"))
                    return

            self.loading_popup.progress(80)

            save_path = self.browse_save()

            if not save_path:
                self.loading_popup.dismiss()
                WarningPopup().open("Penyimpanan dokumen dibatalkan!")
                self.randomization_result_description_layout.add_widget(DescriptionLabel("Status", "GAGAL"))
                self.randomization_result_description_layout.add_widget(
                    DescriptionLabel("Alasan", "Penyimpanan dokumen dibatalkan!"))
                return

            if self.csv_preprocessor.matrixToCSV(randomizer.getPerturbedDataset(), save_path):
                self.loading_popup.dismiss()
                WarningPopup().open(
                    "Tolong menutup dokumen yang dipilih yaitu " + save_path)
                self.randomization_result_description_layout.add_widget(DescriptionLabel("Status", "GAGAL"))
                self.randomization_result_description_layout.add_widget(DescriptionLabel("Alasan",
                                                                                         "Sudah ada dokumen yang mempunyai nama yang sama yaitu " + save_path + " dan dibuka oleh program lain!\nMohon ditutup "
                                                                                                                                                                "terlebih dahulu!"))
                return

            self.randomization_result_description_layout.add_widget(DescriptionLabel("Status", "BERHASIL"))
            self.randomization_result_description_layout.add_widget(
                DescriptionLabel("Lokasi Dokumen", save_path))
            self.randomization_result_description_layout.add_widget(
                DescriptionLabel("Jumlah Kolom", str(randomizer.getPerturbedDataset().getNumberOfColumns())))
            if self.technique_spinner.text == "Random Projection Perturbation":
                self.randomization_result_description_layout.add_widget(
                    DescriptionLabel("Nilai variabel epsilon yang dipakai", str(randomizer.getEpsilon())))
                self.randomization_result_description_layout.add_widget(
                    DescriptionLabel("nilai K yang dipakai", str(randomizer.getK())))

            self.loading_popup.progress(100)
            self.loading_popup.dismiss()
            WarningPopup().open(self.technique_spinner.text + " berhasil diterapkan pada dataset yang dipilih!")
        except Exception as e:
            self.loading_popup.dismiss()
            WarningPopup().open(str(e))
            self.randomization_result_description_layout.add_widget(DescriptionLabel("Status", "GAGAL"))
            self.randomization_result_description_layout.add_widget(DescriptionLabel("Alasan", str(e)))
            return


class WarningPopup(Popup):
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
