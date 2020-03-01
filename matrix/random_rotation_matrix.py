from matrix.matrix import Matrix
from scipy.stats import special_ortho_group


class RandomRotationMatrix():
    @staticmethod
    def generate(dimension):
        return Matrix(special_ortho_group.rvs(dim=dimension))
