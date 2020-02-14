from . import matrix


class RandomProjectionMatrix(matrix.Matrix):
    def __init__(self, numberOfRows, numberOfColumns, k):
        self._k = k
