from . import perturbation
import numpy as np


class RandomProjectionPerturbation(perturbation.Perturbation):
    def __init__(self, dataset, epsilon, dimensionTarget):
        super(dataset)
        self._epsilon = epsilon
        self._dimensionTarget = dimensionTarget

        self._k = None
        self.calculateK()

        self._randomProjectionMatrix = np.matrix(None)
        self.generateRandomProjectionMatrix()

    def generateRandomProjectionMatrix(self):
        pass

    def getRandomProjectionMatrix(self):
        return self._randomProjectionMatrix

    def perturbDataset(self):
        pass

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

    def calculateK(self):
        pass

    def checkMinDim(self):
        pass
