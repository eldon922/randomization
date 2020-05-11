from .perturbation import Perturbation
from sklearn.random_projection import johnson_lindenstrauss_min_dim, GaussianRandomProjection
from matrix.matrix import Matrix


class RandomProjectionPerturbation(Perturbation):
    def __init__(self, dataset, epsilon, k=0, randomProjectionMatrix=False):
        super().__init__(dataset)
        self._epsilon = epsilon
        self._k = k

        self._MinK = None
        self.calculateMinK()

        self._transformer = self.GaussianRandomProjection(n_components=k, eps=epsilon,
                                                          randomProjectionMatrix=randomProjectionMatrix)

    def perturbDataset(self):
        self._perturbedDataset = Matrix(self._transformer.fit_transform(self._dataset.getRawMatrix()))

    def getEpsilon(self):
        return self._transformer.eps

    def getMinK(self):
        return self._MinK

    def calculateMinK(self):
        self._MinK = johnson_lindenstrauss_min_dim(
            self._dataset.getNumberOfRows(), self._epsilon)

    def checkMinK(self):
        return self._MinK < self._dataset.getNumberOfColumns()

    def checkVariableK(self):
        return self._MinK <= self._k < self._dataset.getNumberOfColumns()

    class GaussianRandomProjection(GaussianRandomProjection):
        def __init__(self, n_components, eps, randomProjectionMatrix):
            super().__init__(n_components=n_components, eps=eps)
            self._randomProjectionMatrix = randomProjectionMatrix

        def _make_random_matrix(self, n_components, n_features):
            # TODO kasih if?
            return self._randomProjectionMatrix.getRawMatrix()
