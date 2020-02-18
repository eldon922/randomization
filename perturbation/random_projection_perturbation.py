from .perturbation import Perturbation
import numpy as np
from sklearn.random_projection import johnson_lindenstrauss_min_dim, GaussianRandomProjection
from matrix.matrix import Matrix


class RandomProjectionPerturbation(Perturbation):
    def __init__(self, dataset, epsilon, dimensionTarget):
        super().__init__(dataset)
        self._epsilon = epsilon
        self._dimensionTarget = dimensionTarget

        self._k = self.generateK()

    #     self._randomProjectionMatrix = self.generateRandomProjectionMatrix()

    # def generateRandomProjectionMatrix(self):
    #     return 0

    # def getRandomProjectionMatrix(self):
    #     return self._randomProjectionMatrix

    def perturbDataset(self):
        if self.checkMinDim():
            transformer = GaussianRandomProjection(eps=self._epsilon)
            self._perturbedDataset = Matrix(transformer.fit_transform(self._dataset.getMatrix()))
            return True
        else:
            return False

    def getEpsilon(self):
        return self.epsilon

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def getDimensionTarget(self):
        return self._dimensionTarget

    def setDimensionTarget(self, dimensionTarget):
        self._dimensionTarget = dimensionTarget

    def getK(self):
        return self._k

    def generateK(self):
        return johnson_lindenstrauss_min_dim(
            self._dataset.getNumberOfRows(), self._epsilon)

    def checkMinDim(self):
        return self._k < self._dataset.getNumberOfColumns() and self._dimensionTarget < self._k
