import ntpath
import os

from numpy import array
from pandas import DataFrame, read_csv
from matrix.matrix import Matrix


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class CSVPreprocessor:
    def readCSV(self, filePath):
        self._filePath = filePath
        self._dataCSV = read_csv(self._filePath)

        self._matrix = None
        self._nameOfColumns = None
        self._resultFilePath = None

    def dropColumn(self, columnName):
        del self._dataCSV[columnName]
        return True

    def csvToMatrix(self):
        self._matrix = Matrix(array(self._dataCSV.values))
        self._nameOfColumns = self._dataCSV.columns
        return self._matrix

    def getFilePath(self):
        return self._filePath

    def getNameOfColumns(self):
        return self._nameOfColumns

    def getFileName(self):
        return path_leaf(self._filePath)

    def getResultFileName(self):
        return path_leaf(self._resultFilePath)

    def matrixToCSV(self, matrix, newFilePath):
        if matrix.getNumberOfColumns() != self._nameOfColumns.size:
            self._resultFilePath = newFilePath + "/projection_randomized_" + path_leaf(self._filePath)
            df = DataFrame(matrix.getRawMatrix())
        else:
            self._resultFilePath = newFilePath + "/rotation_randomized_" + path_leaf(self._filePath)
            df = DataFrame(matrix.getRawMatrix(), columns=self._nameOfColumns)

        if os.path.isfile(self._resultFilePath):
            return True

        df.to_csv(self._resultFilePath, index=False)
        return False
