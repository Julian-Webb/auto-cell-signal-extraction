from collections import defaultdict

import pandas as pd
import numpy as np
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.cluster import KMeans
from src.utils.decorators import message_and_time


@message_and_time('')
def agglomerative_clustering(roi_distances: pd.DataFrame, rois: np.array, max_clusters: int):
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


@message_and_time('')
def k_means(signals_df: pd.DataFrame, n_clusters: int):
    """
    Performs k-means clustering on the signals of the ROIs.
    :param signals_df:
    :param n_clusters:
    :return:
    """
    kmeans = KMeans(n_clusters=n_clusters, n_init='auto')
    kmeans.fit(signals_df.T)

    # which cluster each ROI belongs to
    roi_cluster_dict = dict(zip(signals_df.columns, kmeans.labels_))

    # create a list of the ROIs in each cluster
    clusters = defaultdict(list)
    for roi, cluster in roi_cluster_dict.items():
        clusters[cluster].append(roi)

    return clusters, n_clusters, roi_cluster_dict

@message_and_time('')
def k_means_spatial_naive(signals_df: pd.DataFrame, n_clusters: int):
    """
    Performs k-means clustering while taking the signals and the spatial location of the ROIs into account.
    :param signals_df:
    :param n_clusters:
    :return:
    """
    rois = signals_df.columns
    # create DataFrame for spatial locations
    spatial_indexes = {roi: [roi.center_pixels().x, roi.center_pixels().y] for roi in rois}
    spatial_indexes = pd.DataFrame(spatial_indexes, index=['x_center', 'y_center'])

    # Normalize the signals
    # We do this, so that they are not taken into account too much
    max_absolute_signal_value = signals_df.abs().max().max()
    normalized_signals = signals_df / max_absolute_signal_value

    # concatenate signals and spatial indexes
    signals_indexes = pd.concat([spatial_indexes, normalized_signals])
    # we convert the index to str because KMeans doesn't accept mixed indexes
    signals_indexes.index = signals_indexes.index.astype(str)

    kmeans = KMeans(n_clusters=n_clusters, n_init='auto')
    # The DataFrame needs to be transposed because a format of (n_samples, n_features) is expected
    kmeans.fit(signals_indexes.T)

    # which cluster each ROI belongs to
    roi_cluster_dict = dict(zip(rois, kmeans.labels_))

    # create a list of the ROIs in each cluster
    clusters = defaultdict(list)
    for roi, cluster in roi_cluster_dict.items():
        clusters[cluster].append(roi)

    return clusters, n_clusters, roi_cluster_dict


@message_and_time('')
def k_means_spatial_weighted(signals_df: pd.DataFrame, n_clusters: int, n_frames: int, spatial_weight: float):
    """
    Performs k-means clustering while taking the signals and the spatial location of the ROIs into account. The spatial
    location can be taken into account more or less strongly depending on `spatial_weight`.
    :param signals_df:
    :param n_clusters: The number of clusters that should be made
    :param n_frames: The number of frames in the recording
    :param spatial_weight: The factor by which the spatial location is multiplied to increase its weight compared to the
        signals. The location is taken into account more strongly than the signals if spatial_weight >1 and less strongly
        if it is <1. If it's 1, they will be weighed equally.
    :return:
    """
    rois = signals_df.columns
    # create DataFrame for spatial locations
    roi_centers = pd.DataFrame(
        {roi: [roi.center_cm().x, roi.center_cm().y] for roi in rois},
    )

    # adjust spatial indexes for n_frames and scale by spatial weight
    # (see n_frames_adjustment_1D.ipynb for explanation)
    roi_centers *= np.sqrt(n_frames) * spatial_weight
    roi_centers.index = ['x_location_value', 'y_location_value']

    # Normalizing the signals
    # (see signal_amplitude_adjustment_1D.ipynb for explanation)
    max_amplitude_overall = signals_df.abs().max().max()
    normalized_signals = signals_df / max_amplitude_overall

    signals_and_locations = pd.concat([roi_centers, normalized_signals])
    # we convert the index to str because KMeans doesn't accept mixed indexes
    signals_and_locations.index = signals_and_locations.index.astype(str)

    kmeans = KMeans(n_clusters=n_clusters, n_init='auto')
    # The DataFrame needs to be transposed because a format of (n_samples, n_features) is expected
    kmeans.fit(signals_and_locations.T)

    # which cluster each ROI belongs to
    roi_cluster_dict = dict(zip(rois, kmeans.labels_))

    # create a list of the ROIs in each cluster
    clusters = defaultdict(list)
    for roi, cluster in roi_cluster_dict.items():
        clusters[cluster].append(roi)

    return clusters, n_clusters, roi_cluster_dict
