from preprocessor.csv_preprocessor import CSVPreprocessor


class ProjectionMatrixPreprocessor:
    def __init__(self):
        self._projectionMatrix = None

    def read_from_csv(self, filePath, dimension):
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
    def save_to_csv(path, projectionMatrix):
        csv_preprocessor = CSVPreprocessor()
        csv_preprocessor.matrixToCSV(projectionMatrix, path)
