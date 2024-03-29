import numpy as np

from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

class Clusterer:
    """class that constructs a model for training"""

    def __init__(self, num_clusters=5, clustering_method='KNN'):
        self.num_clusters = num_clusters
        self.clustering_method = clustering_method
        assert self.clustering_method in ('KNN', 'GMM')
        self.instantiate_model()

    def instantiate_model(self) -> None:
        """create a prediction model"""
        if self.clustering_method == 'KNN':
            self.model = KMeans(n_clusters=self.num_clusters, max_iter=10000)
        elif self.clustering_method == 'GMM':
            self.model = GaussianMixture(n_components=self.num_clusters)
        else:
            raise ValueError("Choose from GMM or KNN")

    def fit(self, data: np.array) -> None:
        self.model.fit(data)

    def predict(self, data: np.array) -> None:
        return self.model.predict(data)

    @property
    def centroids(self) -> np.array:
        """provides information on what pixel intensities correspond to each
        cluster"""
        if self.clustering_method=='KNN':
            return self.model.cluster_centers_
        return self.model.means_

    def collapse_centroids(self, threshold):
        """planned method to allow us to gradually merge centroids that are
        close together. A form of annealing the number of clusters down"""
        raise NotImplementedError
