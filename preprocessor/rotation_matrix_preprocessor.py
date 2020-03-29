from pandas import DataFrame, concat

from matrix.matrix import Matrix
from preprocessor.csv_preprocessor import CSVPreprocessor


class RotationMatrixPreprocessor:
    def __init__(self):
        self._randomTranslationMatrix = None
        self._randomRotationMatrix = None

    def read_from_csv(self, filePath, dimension):
        csvPreprocessor = CSVPreprocessor()
        csvPreprocessor.readCSV(filePath)
        matrix = csvPreprocessor.csvToMatrix()

        if matrix.getNumberOfRows() != dimension + 1 or matrix.getNumberOfColumns() != dimension * 2 + 1:
            return False
        else:
            self._randomRotationMatrix = Matrix(matrix.getRawMatrix()[:dimension, :dimension])
            self._randomTranslationMatrix = Matrix(matrix.getRawMatrix()[:, dimension:])
            return True

    def getRandomRotationMatrix(self):
        return self._randomRotationMatrix

    def getRandomTranslationMatrix(self):
        return self._randomTranslationMatrix

    @staticmethod
    def save_to_csv(path, randomRotationMatrix, randomTranslationMatrix):
        try:
            df1 = DataFrame(randomRotationMatrix.getRawMatrix())
            df2 = DataFrame(randomTranslationMatrix.getRawMatrix())
            df = concat([df1, df2], axis=1)
            df.to_csv(path, index=False)
            return False
        except:
            return True