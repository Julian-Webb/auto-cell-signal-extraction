import numpy as np
import pandas as pd
from scipy.spatial import distance


def estimate_cell_equality(signal_arr: np.array, n_horizontal: int, n_vertical: int):
    """Takes in an array of signals and estimate for each pair whether they are coming from the same cell or not.
    Regarding the inputted array, the first dimension represents the horizontal ROI index,
    the second represents the vertical ROI index,
    and the third represents the frame. The value is the signal.
    Returns a dataframe with the distance-adjusted similarity of each pair of ROIs"""

    roi_indices = [(x, y) for x in range(n_horizontal) for y in range(n_vertical)]
    n_rois = n_horizontal * n_vertical

    # initialize a dataframe to store the estimate equality.
    str_rois = [str(roi) for roi in roi_indices]  # get roi indices as str
    equality_df = pd.DataFrame(np.zeros(shape=(n_rois, n_rois)))
    equality_df.index = str_rois
    equality_df.columns = str_rois

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

            equality_df.at[str(roi1), str(roi2)] = similarity

    return equality_df


def roi_distance(roi1: tuple, roi2: tuple):
    """This is our adjacency measure. If the ROIs are too far apart, they can't be from the same cell, and we needn't
    compare them"""
    return distance.euclidean(roi1, roi2)


def signal_similarity(signal1: np.array, signal2: np.array) -> float:
    """This is our measure for signal similarity."""

    # similarity = cos_similarity[0][0]
    # similarity = 1 - distance.cosine(signal1, signal2)  # cosine similarity (ignores magnitude)

    similarity = cosine_similarity(signal1, signal2)
    return similarity


def cosine_similarity(a, b):
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
