from sklearn.random_projection import GaussianRandomProjection

from matrix.matrix import Matrix


class RandomProjectionMatrix:
    @staticmethod
    def generate(originalDimension, dimensionTarget, epsilon):
        transformer = GaussianRandomProjection(n_components=dimensionTarget, eps=epsilon)
        return Matrix(transformer._make_random_matrix(dimensionTarget, originalDimension))
