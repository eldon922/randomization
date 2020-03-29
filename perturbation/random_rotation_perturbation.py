from .perturbation import Perturbation
from matrix.random_translation_matrix import RandomTranslationMatrix


class RandomRotationPerturbation(Perturbation):
    def __init__(self, dataset, randomTranslationMatrix, randomRotationMatrix):
        super().__init__(dataset)

        self._randomTranslationMatrix = randomTranslationMatrix
        self._randomRotationMatrix = randomRotationMatrix

    def perturbDataset(self):
        dataset_with_ones = RandomTranslationMatrix.addAColumnOfOnes(self._dataset)
        translated_dataset_with_ones = dataset_with_ones.multiply(self._randomTranslationMatrix)
        translated_dataset = RandomTranslationMatrix.removeLastColumn(translated_dataset_with_ones)

        self._perturbedDataset = translated_dataset.multiply(self._randomRotationMatrix)
        return True

    def getRandomTranslationMatrix(self):
        return self._randomTranslationMatrix

    def getRandomRotationMatrix(self):
        return self._randomRotationMatrix
