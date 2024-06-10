import math

import sklearn

import numpy as np
import pandas as pd
from src.utils.ROI import ROI
from src.utils.decorators import message_and_time

# The maximum distance that two signals can have. For cosine distance, it's 2.
_MAX_DISTANCE: float = 2.0

@message_and_time('')
def calculate_roi_distances(signals_df: pd.DataFrame, comp_range_px: int):
    """Takes in the signals of each ROI and calculates a distance measure between each pair or ROIs.
    It takes the spatial distance between the ROIs and the signal similarity into account.

    :param signals_df: A dataframe where each column represents the signal of a ROI
    :param comp_range_px: The spatial ROI comparison range in pixels
    :return: A DataFrame with the computed distance between each pair of ROIs.
    """
    # Create a DataFrame to store the ROI distances
    filtered_rois = signals_df.columns
    distances = pd.DataFrame(_MAX_DISTANCE, columns=filtered_rois, index=filtered_rois, dtype='float64')

    # Calculate cosine distances
    cos_distances = sklearn.metrics.pairwise.cosine_distances(signals_df.T)
    np.fill_diagonal(cos_distances, 0)  # We do this because sklearn is not completely precise.
    cos_distances = pd.DataFrame(cos_distances, columns=filtered_rois, index=filtered_rois)

    # --- ROIs should only be compared if they are within a certain spatial range of each other. ---
    # Compute which ROIs are within range
    comparisons = compute_comparisons(filtered_rois, comp_range_px)

    # If they are, we set the distance to the cosine similarity.
    for roi, within_range in comparisons.items():
        distances.loc[roi, within_range] = distances.loc[within_range, roi] = cos_distances.loc[roi, within_range]

    return distances


def compute_comparisons(filtered_rois: np.array, comp_range_px: int):
    """
    This function computes which comparisons should be made between the ROIs, such that they are only compared within a
    certain spatial distance.

    :param filtered_rois: An array of the ROIs after removing the empty ROIs
    :param comp_range_px: The spatial ROI comparison range in pixels
    :return: A dict with a list of ROIs for each ROI. The list tells us which ROIs it needs to be compared with
    """
    # Convert the pixel distance into a distance of ROI indexes
    # We do this by dividing the range in pixels by the ROI width/height and then rounding it up
    x_range = math.ceil(comp_range_px / ROI.WIDTH_PIXELS)
    y_range = math.ceil(comp_range_px / ROI.HEIGHT_PIXELS)

    # A dict with an entry for each of the filtered ROIs and which other ROIs it should be compared with
    comparisons = {}

    # construct a new empty matrix for the ROIs
    rois_matrix = np.zeros((ROI.N_HORIZONTAL, ROI.N_VERTICAL), dtype=ROI)

    # fill it with the filtered ROIs. Leave the rest blank
    for roi in filtered_rois:
        rois_matrix[roi.x_idx, roi.y_idx] = roi

    # go through each of the filtered ROIs and fill the dictionary by checking which filtered ROIs are within range
    for roi in filtered_rois:
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

        # Select the ROIs within these boundaries
        # We add 1 because the upper boundary is not included when indexing
        within_bounds = rois_matrix[x_left: x_right + 1, y_top: y_bottom + 1]

        # Now we select all the values that are not removed
        rois_within_bounds = within_bounds[within_bounds != 0]

        comparisons[roi] = rois_within_bounds

    return comparisons
