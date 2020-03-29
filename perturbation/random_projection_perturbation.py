from .perturbation import Perturbation
from sklearn.random_projection import johnson_lindenstrauss_min_dim, GaussianRandomProjection
from matrix.matrix import Matrix


class RandomProjectionPerturbation(Perturbation):
    def __init__(self, dataset, epsilon, dimensionTarget=0, randomProjectionMatrix=False):
        super().__init__(dataset)
        self._epsilon = epsilon
        self._dimensionTarget = dimensionTarget

        self._k = None
        self.calculateK()

        self._transformer = self.GaussianRandomProjection(n_components=dimensionTarget, eps=epsilon,
                                                          randomProjectionMatrix=randomProjectionMatrix)

    def perturbDataset(self):
        self._perturbedDataset = Matrix(self._transformer.fit_transform(self._dataset.getRawMatrix()))

    def getEpsilon(self):
        return self._transformer.eps

    def getK(self):
        return self._k

    def calculateK(self):
        self._k = johnson_lindenstrauss_min_dim(
            self._dataset.getNumberOfRows(), self._epsilon)

    def checkK(self):
        return self._k < self._dataset.getNumberOfColumns()

    def checkDimensionTarget(self):
        return self._k <= self._dimensionTarget < self._dataset.getNumberOfColumns()

    class GaussianRandomProjection(GaussianRandomProjection):
        def __init__(self, n_components, eps, randomProjectionMatrix):
            super().__init__(n_components=n_components, eps=eps)
            self._randomProjectionMatrix = randomProjectionMatrix

        def _make_random_matrix(self, n_components, n_features):
            # TODO kasih if?
            return self._randomProjectionMatrix.getRawMatrix()
