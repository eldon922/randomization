from preprocessor.csv_preprocessor import CSVPreprocessor
from perturbation.random_rotation_perturbation import RandomRotationPerturbation
from perturbation.random_projection_perturbation import RandomProjectionPerturbation

if __name__ == "__main__":
    csvPreprocessor = CSVPreprocessor()
    csvPreprocessor.readCSV(
        r'C:\Users\eldon\Desktop\Skripsi 2\test program\iris.csv')
    csvPreprocessor.dropColumn('species')

    dataset = csvPreprocessor.csvToMatrix()

    rotation_randomizer = RandomRotationPerturbation(dataset)
    if rotation_randomizer.perturbDataset():
        csvPreprocessor.matrixToCSV(rotation_randomizer.getPerturbedDataset(
        ), r"C:\Users\eldon\Desktop\Skripsi 2\test program\rotation_randomized.csv")

    projection_randomizer = RandomProjectionPerturbation(dataset, 0.9, 75)
    if projection_randomizer.perturbDataset():
        csvPreprocessor.matrixToCSV(projection_randomizer.getPerturbedDataset(
        ), r"C:\Users\eldon\Desktop\Skripsi 2\test program\projection_randomized.csv")

    pass
