from .perturbation import Perturbation
from matrix.matrix import Matrix
from matrix.random_rotation_matrix import RandomRotationMatrix
from matrix.random_translation_matrix import RandomTranslationMatrix
from numpy import array


class RandomRotationPerturbation(Perturbation):
    def __init__(self, dataset):
        super().__init__(dataset)

        self._randomTranslationMatrix = self.generateRandomTranslationMatrix()
        self._randomRotationMatrix = self.generateRandomRotationMatrix()

    def generateRandomTranslationMatrix(self):
        return RandomTranslationMatrix(self._dataset.getNumberOfColumns())

    def getRandomTranslationMatrix(self):
        return self._randomTranslationMatrix

    def generateRandomRotationMatrix(self):
        return RandomRotationMatrix(self._dataset.getNumberOfColumns())

    def getRandomRotationMatrix(self):
        return self._randomRotationMatrix

    def perturbDataset(self):
        self._perturbedDataset = self._dataset.multiply(self._randomTranslationMatrix).multiply(self._randomRotationMatrix)
        return True
