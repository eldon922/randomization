from numpy.linalg import det


class Matrix:
    def __init__(self, matrix):
        self._matrix = matrix

    def getNumberOfRows(self):
        return self._matrix.shape[0]

    def getNumberOfColumns(self):
        return self._matrix.shape[1]

    def multiply(self, multiplierMatrix):
        self._matrix = self._matrix @ multiplierMatrix.getMatrix()
        return self

    def get(self, row, col):
        return self._matrix[row][col]

    def getMatrix(self):
        return self._matrix

    def determinant(self):
        return det(self._matrix)

    def transpose(self):
        self._matrix = self._matrix.T
        return self
