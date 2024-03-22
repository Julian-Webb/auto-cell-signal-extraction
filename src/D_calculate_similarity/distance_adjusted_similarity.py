import numpy as np
import pandas as pd
from scipy.spatial import distance

from src.utils.roi_names import roi_indexes_to_compact_label


def distance_adjusted_similarity(signal_arr: np.array, n_horizontal: int, n_vertical: int):
    """Takes in an array of signals and estimate for each pair whether they are coming from the same cell or not.
    Regarding the inputted array, the first dimension represents the horizontal ROI index,
    the second represents the vertical ROI index,
    and the third represents the frame. The value is the signal.
    Returns a dataframe with the distance-adjusted similarity of each pair of ROIs"""

    # TODO improve the way the similarity works with the new ROI class (especially readibility)
    # TODO improve the quality of the metric
    roi_indices = [(x, y) for x in range(n_horizontal) for y in range(n_vertical)]
    n_rois = n_horizontal * n_vertical

    # initialize a dataframe to store the distance-adjusted similarity
    str_rois = [roi_indexes_to_compact_label(roi[0], roi[1]) for roi in roi_indices]  # get roi indices as str
    dist_adj_sim = pd.DataFrame(np.zeros(shape=(n_rois, n_rois)))
    dist_adj_sim.index = str_rois
    dist_adj_sim.columns = str_rois

    # loop through each pair of ROIs and compute the similarity measure
    for roi1 in roi_indices:
        for roi2 in roi_indices:
            # estimate roi similarity
            if roi1 == roi2:
                # if it's the same roi
                similarity = 1
            else:
                # else calculate the similarity
                dist = roi_distance(roi1, roi2)

                signal1 = signal_arr[roi1[0], roi1[1], :]
                signal2 = signal_arr[roi2[0], roi2[1], :]
                signal_sim = signal_similarity(signal1, signal2)

                similarity = signal_sim / dist

            roi1_str = roi_indexes_to_compact_label(roi1[0], roi1[1])
            roi2_str = roi_indexes_to_compact_label(roi2[0], roi2[1])
            dist_adj_sim.at[roi1_str, roi2_str] = similarity

    return dist_adj_sim


def roi_distance(roi1: tuple, roi2: tuple):
    """This is our adjacency measure. If the ROIs are too far apart, they can't be from the same cell, and we needn't
    compare them"""
    dist = distance.euclidean(roi1, roi2)
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
