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

    rois_flat = rois.flatten()
    n_rois = ROI.N_HORIZONTAL * ROI.N_VERTICAL

    # initialize a dataframe to store the ROI distance matrix.
    pairwise_distances = pd.DataFrame(np.zeros((n_rois, n_rois)), columns=rois_flat, index=rois_flat)

    # find the maximum spatial distance. We normalize by this
    max_spatial_dist = roi_spatial_distance(rois_flat[0], rois_flat[-1])

    # loop through each pair of ROIs and compute the distance
    for roi1 in rois_flat:
        for roi2 in rois_flat:
            # NOTE: distance is initialized as 0
            if roi1 != roi2:
                spatial_dist = roi_spatial_distance(roi1, roi2)

                signal_sim = signal_similarity(signals_df[roi1], signals_df[roi2])

                # spatial distance is from 0 to infinity.  -> high value increases roi distance
                # Signal similarity is from 0 to 1. -> higher value decreases roi distance
                if signal_sim == 0:
                    distance = max_spatial_dist  # TODO find cleaner solution
                else:
                    distance = spatial_dist / signal_sim

                pairwise_distances.at[roi1, roi2] = distance

    # normalize with the maximum spatial distance
    return pairwise_distances / max_spatial_dist


def roi_spatial_distance(roi1: ROI, roi2: ROI):
    """This is our adjacency measure. If the ROIs are too far apart, they can't be from the same cell, and we needn't
    compare them"""
    dist = distance.euclidean((roi1.x_idx, roi1.y_idx), (roi2.x_idx, roi2.y_idx))
    return 0.01 * dist ** 2 + 1


def signal_similarity(signal1: np.array, signal2: np.array) -> float:
    """This is our measure for signal similarity."""

    # similarity = cos_similarity[0][0]
    # similarity = 1 - distance.cosine(signal1, signal2)  # cosine similarity (ignores magnitude)

    similarity = cosine_similarity(signal1, signal2)
    return similarity


def cosine_similarity(a: np.array, b: np.array):
    dot_product = np.dot(a, b)
    magnitude_a = np.linalg.norm(a)
    magnitude_b = np.linalg.norm(b)

    # if the magnitude of vectors a or b is 0, the resulting division leads to an error.
    # If that's the case, the ROI is measuring an empty space, and we can consider the similarity minimal (0).
    # NOTE: we won't have any negative similarity because signal values are always non-negative.
    if magnitude_a == 0 or magnitude_b == 0:
        return 0
    cos_sim = dot_product / (magnitude_a * magnitude_b)

    return cos_sim
