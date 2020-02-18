from matrix.matrix import Matrix
from numpy import identity, append, ones
from random import randint


class RandomTranslationMatrix(Matrix):
    def __init__(self, dimension):
        matrix = identity(dimension)
        matrix[-1][:-1] = [randint(0,100) for x in matrix[-1][:-1]]

        super().__init__(matrix)

    @staticmethod
    def addAColumnOfOnes(matrix):
        matrixTransposed = matrix.transpose()
        return Matrix(append(matrixTransposed.getMatrix(), ones((1, matrixTransposed.getNumberOfColumns())), axis=0)).transpose()

    @staticmethod
    def removeLastColumn(matrix):
        return Matrix(matrix.transpose().getMatrix()[:-1].T)
