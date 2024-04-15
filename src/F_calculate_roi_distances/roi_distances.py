import numpy as np
import pandas as pd
from scipy.spatial import distance

from src.utils.ROI import ROI


def roi_distances(signals_df: pd.DataFrame, rois: np.array):
    """Takes in the signals of each ROI and calculates a distance measure between each pair or ROIs.
    It takes the spatial distance between the ROIs and the signal similarity into account.

    :param signals_df: A dataframe where each column represents the signal of a ROI
    :param rois: An array containing all the ROI objects.

    :return: A DataFrame with the computed distance between each pair of ROIs.
    """

    # TODO improve the quality of the metric

    # initialize a dataframe to store the ROI distance matrix.
    n_rois = len(rois)
    spatial_distances = pd.DataFrame(np.zeros((n_rois, n_rois)), columns=rois, index=rois)
    signal_similarities = pd.DataFrame(np.zeros((n_rois, n_rois)), columns=rois, index=rois)

    # Determine which ROIs should be compared.
    # They should only be compared if they are within a certain distance of each other
    # rois_: np.array = rois.copy()

    # loop through each pair of ROIs and compute distance
    for roi1 in rois:
        for roi2 in rois:
            # from 0 to inf, the higher, the higher the dist
            spatial_distances.at[roi1, roi2] = roi_spatial_distance(roi1, roi2)

            # from -1 to 1, the higher, the lower the dist
            signal_similarities.at[roi1, roi2] = signal_similarity(signals_df[roi1], signals_df[roi2])

    # we now cut off any similarities <0 and just make them 0 because these signals aren't considered to belong to the
    # same cell anyway.
    signal_similarities[signal_similarities < 0] = 0
    signal_distances = 1 - signal_similarities

    roi_distances_ = spatial_distances * signal_distances

    # ## Normalize the distances between 0 and 1 ###
    # To do this, we normalize by the maximum absolute value. That gives us values between -1 and 1.
    # Then we add 1 and divide by 2 to get values between 0 and 1.
    max_dist = roi_distances_.abs().max(axis=None)
    norm_distances = roi_distances_ / max_dist

    # make the diagonal 0 (sometimes there are tiny non-zero values...)
    for roi in rois:
        norm_distances.at[roi, roi] = 0

    return norm_distances


def roi_spatial_distance(roi1: ROI, roi2: ROI):
    """This is our adjacency measure. If the ROIs are too far apart, they can't be from the same cell, and we needn't
    compare them"""
    dist = distance.euclidean((roi1.x_idx, roi1.y_idx), (roi2.x_idx, roi2.y_idx))
    return 0.01 * dist ** 2 + 1


def signal_similarity(signal1: np.array, signal2: np.array) -> float:
    """This is our measure for signal distance."""

    # similarity = cos_similarity[0][0]
    # similarity = 1 - distance.cosine(signal1, signal2)  # cosine similarity (ignores magnitude)

    similarity = cosine_similarity(signal1, signal2)

    # cos similarity can be between -1 and 1. All values from in [-1, 0] should become 0 because these will be treated
    # as different clusters anyway.

    return similarity


def cosine_similarity(a: np.array, b: np.array):
    dot_product = np.dot(a, b)
    magnitude_a = np.linalg.norm(a)
    magnitude_b = np.linalg.norm(b)

    # if the magnitude of vectors a or b is 0, the resulting division leads to an error.
    # If that's the case, the ROI is measuring an empty space, and we can consider the similarity minimal (0).
    if magnitude_a == 0 or magnitude_b == 0:
        return 0
    cos_sim = dot_product / (magnitude_a * magnitude_b)

    return cos_sim
