from .matrix import Matrix
from numpy import identity, append, ones
from random import uniform


class RandomTranslationMatrix:
    @staticmethod
    def generate(dimension):
        matrix = identity(dimension)
        matrix[-1][:-1] = [uniform(0, 100) for x in matrix[-1][:-1]]

        return Matrix(matrix)

    @staticmethod
    def addAColumnOfOnes(matrix):
        matrixTransposed = matrix.transpose()
        return Matrix(append(matrixTransposed.getRawMatrix(), ones((1, matrixTransposed.getNumberOfColumns())),
                      axis=0)).transpose()

    @staticmethod
    def removeLastColumn(matrix):
        return Matrix(matrix.transpose().getRawMatrix()[:-1].T)
