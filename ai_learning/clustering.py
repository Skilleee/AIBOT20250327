import numpy as np
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering

def cluster_assets_kmeans(X: np.ndarray, n_clusters: int = 3) -> np.ndarray:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)
    return clusters

def cluster_assets_dbscan(X: np.ndarray, eps: float = 0.5, min_samples: int = 5) -> np.ndarray:
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    clusters = dbscan.fit_predict(X)
    return clusters

def cluster_assets_hierarchical(X: np.ndarray, n_clusters: int = 3) -> np.ndarray:
    hier = AgglomerativeClustering(n_clusters=n_clusters)
    clusters = hier.fit_predict(X)
    return clusters
