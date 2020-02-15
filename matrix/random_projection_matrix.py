from . import matrix


class RandomProjectionMatrix(matrix.Matrix):
    def __init__(self, dimension, dimensionTarget, k):
        self._k = k
