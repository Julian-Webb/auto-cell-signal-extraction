import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering

from src.utils.roi_names import roi_linear_index_to_compact_label, roi_linear_index_to_indexes


def cluster_rois(roi_similarity: pd.DataFrame, signals_arr: np.array, similarity_threshold: float, n_horizontal: int,
                 n_vertical, n_frames):
    """This function takes in a dataframe where each value is the similarity of a pair of ROIs.
    It then clusters the ROIs that are similar enough, based on the specified threshold.
    The output is a list of each cluster and which ROIs it contains."""

    # convert similarity into distance
    roi_dist = -roi_similarity + 1

    n_clusters = 5

    # cluster the ROIs with Agglomerative Clustering
    # clustering = AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage='average')
    # roi_cluster_associations = clustering.fit_predict(roi_dist)

    # ########## testing #########################
    flattened = signals_arr.reshape((n_horizontal * n_vertical, n_frames), order='C')
    clustering = AgglomerativeClustering(n_clusters=n_clusters, metric='euclidean', linkage='average')
    roi_cluster_associations = clustering.fit_predict(flattened)

    ###########################################################################

    rois_clusters_dict = {roi_linear_index_to_indexes(lin_idx, n_vertical): cluster for lin_idx, cluster in
                          enumerate(roi_cluster_associations)}

    # create a list of the ROIs in each cluster
    clusters = [[] for _ in range(n_clusters)]
    for roi_idx, cluster_idx in enumerate(roi_cluster_associations):
        clusters[cluster_idx].append(roi_linear_index_to_indexes(roi_idx, n_vertical))

    return clusters, n_clusters, rois_clusters_dict
