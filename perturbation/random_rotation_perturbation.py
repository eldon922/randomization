from . import perturbation
import numpy as np


class RandomRotationPerturbation(perturbation.Perturbation):
    def __init__(self, dataset):
        super(dataset)

        self._randomTranslationMatrix = np.matrix(None)
        self.generateRandomTranslationMatrix()

        self._randomRotationMatrix = np.matrix(None)
        self.generateRandomRotationMatrix()

    def generateRandomTranslationMatrix(self):
        pass

    def getRandomTranslationMatrix(self):
        return self._randomTranslationMatrix

    def generateRandomRotationMatrix(self):
        pass

    def getRandomRotationMatrix(self):
        return self._randomRotationMatrix

    def perturbDataset(self):
        pass
