from abc import ABC, abstractmethod


class Perturbation(ABC):
    def __init__(self, dataset):
        self._dataset = dataset
        self._perturbedDataset = None

    def getOriginalDataset(self):
        return self._dataset

    def getPerturbedDataset(self):
        return self._perturbedDataset

    def setDataset(self, dataset):
        self._dataset = dataset

    @abstractmethod
    def perturbDataset(self):
        pass
