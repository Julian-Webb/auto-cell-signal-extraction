from collections import defaultdict

import pandas as pd
import numpy as np
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, fcluster

from src.utils.decorators import message_and_time


@message_and_time('')
def cluster_rois(roi_distances: pd.DataFrame, rois: np.array, max_clusters: int):
    """This function takes in a dataframe where each value is the similarity of a pair of ROIs.
    It then clusters the ROIs that are similar enough, based on the specified threshold.
    The output is a list of each cluster and which ROIs it contains."""

    # Agglomerative clustering using scipy
    # condense symmetrical distance matrix into vector
    dist_vector = squareform(roi_distances)

    # cluster the ROIs with Agglomerative Clustering
    # the resulting matrix clustering_steps is interpreted as follows:
    # one row for each iteration
    # Each row contains 4 values:
    # the first two are the clusters that were merged
    # the third is the distance between these clusters
    # the fourth is the number samples in this new cluster
    # TODO if we specify max clusters, I might be able to specify this here and reduce time
    clustering_steps = linkage(dist_vector, method='average')

    roi_cluster_associations = fcluster(clustering_steps, max_clusters, criterion='maxclust')

    roi_cluster_associations -= 1  # we subtract 1 because otherwise the cluster indexes start at 1 (rather than 0)

    # with sklearn
    # clustering = AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage='average')
    # roi_cluster_associations = clustering.fit_predict(roi_dist)

    # create a dictionary with ROIs as keys and clusters as values
    roi_cluster_dict = {}
    for i, roi in enumerate(rois):
        # TODO make sure the linear index is using the right major (row/col)
        roi_cluster_dict[roi] = roi_cluster_associations[i]

    # create a list of the ROIs in each cluster
    clusters = defaultdict(list)
    for roi, cluster in roi_cluster_dict.items():
        clusters[cluster].append(roi)

    n_clusters = len(clusters)

    return clusters, n_clusters, roi_cluster_dict, clustering_steps
