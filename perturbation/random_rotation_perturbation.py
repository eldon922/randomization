from .perturbation import Perturbation
from matrix.random_rotation_matrix import RandomRotationMatrix
from matrix.random_translation_matrix import RandomTranslationMatrix


class RandomRotationPerturbation(Perturbation):
    def __init__(self, dataset):
        super().__init__(dataset)

        self._randomTranslationMatrix = None
        self.generateRandomTranslationMatrix()
        self._randomRotationMatrix = None
        self.generateRandomRotationMatrix()

    def perturbDataset(self):
        dataset_with_ones = RandomTranslationMatrix.addAColumnOfOnes(self._dataset)
        translated_dataset_with_ones = dataset_with_ones.multiply(self._randomTranslationMatrix)
        translated_dataset = RandomTranslationMatrix.removeLastColumn(translated_dataset_with_ones)

        self._perturbedDataset = translated_dataset.multiply(self._randomRotationMatrix)
        return True

    def getRandomTranslationMatrix(self):
        return self._randomTranslationMatrix

    def generateRandomTranslationMatrix(self):
        self._randomTranslationMatrix = RandomTranslationMatrix.generate(self._dataset.getNumberOfColumns() + 1)

    def getRandomRotationMatrix(self):
        return self._randomRotationMatrix

    def generateRandomRotationMatrix(self):
        self._randomRotationMatrix = RandomRotationMatrix.generate(self._dataset.getNumberOfColumns())
