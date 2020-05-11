from pandas import DataFrame

from preprocessor.csv_preprocessor import CSVPreprocessor


class ProjectionMatrixPreprocessor:
    def __init__(self):
        self._projectionMatrix = None

    def readFromCSV(self, filePath, dimension):
        csvPreprocessor = CSVPreprocessor()
        csvPreprocessor.readCSV(filePath)
        matrix = csvPreprocessor.csvToMatrix()
        if matrix.getNumberOfColumns() != dimension or matrix.getNumberOfRows() >= dimension:
            return False
        else:
            self._projectionMatrix = matrix
            return True

    def getProjectionMatrix(self):
        return self._projectionMatrix

    @staticmethod
    def saveToCSV(path, projectionMatrix):
        try:
            df = DataFrame(projectionMatrix.getRawMatrix())
            df.to_csv(path, index=False)
            return False
        except:
            return True
