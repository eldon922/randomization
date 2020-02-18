from .perturbation import Perturbation
from matrix.matrix import Matrix, RandomTranslationMatrix, RandomRotationMatrix
from numpy import array


class RandomRotationPerturbation(Perturbation):
    def __init__(self, dataset):
        super(dataset)

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
        self._perturbedDataset = self._dataset @ self._randomTranslationMatrix @ self._randomRotationMatrix
