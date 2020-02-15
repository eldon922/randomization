import numpy as np
import pandas as pd

class CSVPreprocessor:
    def readCSV(self, filePath):
        self._filePath = filePath
        self._dataCSV = pd.read_csv(self._filePath)
        self._matrix = np.array(self._dataCSV.values)
        self._nameOfColumns = self._dataCSV.columns

    def csvToMatrix(self):
        return self._matrix

    def getFilePath(self):
        return self._filePath

    def getNameOfColumns(self):
        return self._nameOfColumns 

    def matrixToCSV(self, matrix, newFilePath):
        df = pd.DataFrame(matrix, columns = self._nameOfColumns)
        df.to_csv(newFilePath, index=False)