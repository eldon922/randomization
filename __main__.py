from preprocessor import csv_preprocessor

if __name__ == "__main__":
    csvPreprocessor = csv_preprocessor.CSVPreprocessor()
    csvPreprocessor.readCSV(r'E:\College\7th Semester\Skripsi 1\test program\iris.csv')
    csvPreprocessor.matrixToCSV(csvPreprocessor.csvToMatrix(), r"E:\College\7th Semester\Skripsi 1\test program\randomized.csv")
    pass
