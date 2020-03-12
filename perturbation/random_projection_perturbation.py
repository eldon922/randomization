from .perturbation import Perturbation
from sklearn.random_projection import johnson_lindenstrauss_min_dim, GaussianRandomProjection
from matrix.matrix import Matrix


class RandomProjectionPerturbation(Perturbation):
    def __init__(self, dataset, epsilon, dimensionTarget):
        super().__init__(dataset)
        self._epsilon = epsilon
        self._dimensionTarget = dimensionTarget

        self._k = None
        self.calculateK()

    def perturbDataset(self):
        transformer = GaussianRandomProjection(n_components=self._dimensionTarget, eps=self._epsilon)
        self._perturbedDataset = Matrix(transformer.fit_transform(self._dataset.getMatrix()))

    def getEpsilon(self):
        return self.epsilon

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def getK(self):
        return self._k

    def calculateK(self):
        self._k = johnson_lindenstrauss_min_dim(
            self._dataset.getNumberOfRows(), self._epsilon)

    def checkK(self):
        return self._k < self._dataset.getNumberOfColumns()

    def checkDimensionTarget(self):
        return self._k <= self._dimensionTarget <= self._dataset.getNumberOfColumns()

    def setDimensionTarget(self, dimensionTarget):
        self._dimensionTarget = dimensionTarget

    def getDimensionTarget(self):
        return self._dimensionTarget
