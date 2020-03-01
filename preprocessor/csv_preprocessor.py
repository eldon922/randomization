from numpy import array
from pandas import DataFrame, read_csv
from matrix.matrix import Matrix

class CSVPreprocessor:
    def readCSV(self, filePath):
        self._filePath = filePath
        self._dataCSV = read_csv(self._filePath)
        
        self._matrix = None
        self._nameOfColumns = None

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

    def matrixToCSV(self, matrix, newFilePath):
        if matrix.getNumberOfColumns() != self._nameOfColumns.size:
            df = DataFrame(matrix.getMatrix())
        else:
            df = DataFrame(matrix.getMatrix(), columns = self._nameOfColumns)

        df.to_csv(newFilePath, index=False)