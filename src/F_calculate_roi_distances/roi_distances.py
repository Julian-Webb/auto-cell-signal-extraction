import concurrent.futures
import math
import multiprocessing

import numpy as np
import pandas as pd
from scipy.spatial import distance
from src.utils.ROI import ROI


def roi_distances(signals_df: pd.DataFrame, comp_range_px: int):
    """Takes in the signals of each ROI and calculates a distance measure between each pair or ROIs.
    It takes the spatial distance between the ROIs and the signal similarity into account.

    :param signals_df: A dataframe where each column represents the signal of a ROI
    :param comp_range_px: The spatial ROI comparison range in pixels
    :return: A DataFrame with the computed distance between each pair of ROIs.
    """

    # Determine which ROIs should be compared based on the adjacency
    filtered_rois = signals_df.columns
    comparisons = compute_comparisons(filtered_rois, comp_range_px)

    # Initialize a DataFrame to store the ROI distances
    # we initialize all distance as maximal (1)
    distances = pd.DataFrame(1.0, columns=filtered_rois, index=filtered_rois)
    # make the diagonal 0
    for roi in filtered_rois:
        distances.loc[roi, roi] = 0

    # --- Concurrently calculate ROI distances ---
    # create a dict which is shared between processes and stores the distances
    manager = multiprocessing.Manager()
    shared_dists = manager.dict()

    # create processes
    processes = []
    for roi, compare_to in comparisons.items():
        partial_signal_df = signals_df[[roi, *compare_to]]
        p = multiprocessing.Process(target=distance_for_one_roi,
                                    args=(roi, compare_to, shared_dists, partial_signal_df))
        processes.append(p)
        p.start()

    # wait for all processes to finish
    for p in processes:
        p.join()

    # enter the computed distances into the original DataFrame
    for key, dist in shared_dists.items():
        roi1, roi2 = key
        distances.loc[roi1, roi2] = distances.loc[roi2, roi1] = dist  # enter it in both permutations

    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     tmp = 0  # TODO delete
    #
    #     # executor.map(lambda roi: distance_for_one_roi(roi, comparisons, distances, signals_df), comparisons.keys())
    #
    #     for roi in comparisons.keys():
    #         if tmp == 0:
    #             executor.submit(distance_for_one_roi, roi, comparisons, distances, signals_df)
    #         tmp += 1
    #
    #     # wait for all processes to finish
    #     executor.shutdown(wait=True) # TODO delete this (already handeled by context handler)

    # Loop through each ROI and fill the DataFrame with the distances to the other ROIs
    # for roi1, compare_to in comparisons.items():
    #     for roi2 in compare_to:
    #         # We bound the similarity to 0 because we care about negative similarity - these signals don't belong to the
    #         # same cell anyway
    #         similarity = max(0.0, signal_similarity(signals_df[roi1], signals_df[roi2]))
    #         dist = 1 - similarity
    #         distances.loc[roi1, roi2] = dist
    #         distances.loc[roi2, roi1] = dist

    return distances


def compute_comparisons(filtered_rois: np.array, comp_range_px: int):
    """
    This function computes which comparisons should be made between the ROIs, such that they are only compared within a
    certain spatial distance and only in one order of comparisons.

    E.g. if the distance between ROI(0;0) and ROI(1;1) is computed in that order, then it should not be computed in the
    order ROI(1;1) vs. ROI(0;0), because these are equivalent, and we want to save resources.

    *NOTE*: Not all the filtered ROIs will necessarily be contained in the output as keys. This is because ROIs are only
    contained if they need to be compared to another ROI, and they are first in order.

    :param filtered_rois: An array of the ROIs after removing the empty ROIs
    :param comp_range_px: The spatial ROI comparison range in pixels
    :return: A dict with a list of ROIs for each ROI. The list tells us which ROIs it needs to be compared with
    """
    # Convert the pixel distance into a distance of ROI indexes
    # We do this by dividing the range in pixels by the ROI width/height and then rounding it up
    x_range = math.ceil(comp_range_px / ROI.WIDTH)
    y_range = math.ceil(comp_range_px / ROI.HEIGHT)

    # A dict with an entry for each of the filtered ROIs and which other ROIs it should be compared with
    comparisons = {}

    # construct a new empty matrix for the ROIs
    rois_matrix = np.zeros((ROI.N_HORIZONTAL, ROI.N_VERTICAL), dtype=ROI)

    # fill it with the filtered ROIs. Leave the rest blank
    for roi in filtered_rois:
        rois_matrix[roi.x_idx, roi.y_idx] = roi

    # go through each of the filtered ROIs and fill the dictionary by checking which filtered ROIs are within range
    for roi in filtered_rois:
        # TODO this could be further optimized if we only looked to the right side with the bounds because we have
        #  already compared the ROIs on the left side. However, this would require filtered_rois to be sorted.

        # Calculate the boundaries of the ROI indexes
        x_left = roi.x_idx - x_range
        y_top = roi.y_idx - y_range
        x_right = roi.x_idx + x_range
        y_bottom = roi.y_idx + y_range

        # They need to be bounded between 0 and the maximum index on that axis
        x_left = max(0, x_left)
        y_top = max(0, y_top)
        x_right = min(x_right, ROI.N_HORIZONTAL - 1)
        y_bottom = min(y_bottom, ROI.N_VERTICAL - 1)

        # We remove this ROI from the matrix, so that it's not compared with itself, and so that the ROIs aren't
        # compared in the reverse order as well (only in one order).
        # E.g. if we compare ROI(0;0) to ROI(1;0), we don't want ROI(1;0) to also be compared to ROI(0;0) in that
        # order because that would be an unnecessary comparison.
        rois_matrix[roi.x_idx, roi.y_idx] = 0

        # Select the ROIs within these boundaries
        # We add 1 because the upper boundary is not included when indexing
        within_bounds = rois_matrix[x_left: x_right + 1, y_top: y_bottom + 1]

        # Now we select all the values that are not removed
        rois_within_bounds = within_bounds[within_bounds != 0]

        # we set this as the dict entry
        if rois_within_bounds.size > 0:
            comparisons[roi] = rois_within_bounds

    return comparisons


def distance_for_one_roi(roi: ROI, compare_to: dict, shared_dists: dict, signals_df: pd.DataFrame):
    """Computes the distances from one ROI to all the ROIs it should be compared to.

    :param roi: The first ROI
    :param compare_to: Which other ROIs the first roi should be compared to
    :param shared_dists: A shared dictionary storing computed distances. It has tuples of ROIs as keys.
    :param signals_df: Contains the signals of each ROI
    """
    for other_roi in compare_to:
        similarity = max(0.0, signal_similarity(signals_df[roi], signals_df[other_roi]))
        dist = 1 - similarity
        shared_dists[(roi, other_roi)] = dist


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
