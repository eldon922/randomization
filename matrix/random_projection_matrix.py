from sklearn.random_projection import GaussianRandomProjection

from matrix.matrix import Matrix


class RandomProjectionMatrix:
    @staticmethod
    def generate(originalDimension, k, epsilon):
        transformer = GaussianRandomProjection(n_components=k, eps=epsilon)
        return Matrix(transformer._make_random_matrix(k, originalDimension))
