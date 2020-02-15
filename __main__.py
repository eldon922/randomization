from preprocessor.csv_preprocessor import CSVPreprocessor

if __name__ == "__main__":
    csvPreprocessor = CSVPreprocessor()
    csvPreprocessor.readCSV(r'E:\College\7th Semester\Skripsi 1\test program\iris.csv')
    csvPreprocessor.matrixToCSV(csvPreprocessor.csvToMatrix(), r"E:\College\7th Semester\Skripsi 1\test program\randomized.csv")
    pass
