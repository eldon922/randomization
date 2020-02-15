from matrix.matrix import Matrix
from scipy.stats import special_ortho_group


class RandomRotationMatrix(Matrix):
    def __init__(self, dimension):
        super(special_ortho_group.rvs(dim=dimension))
