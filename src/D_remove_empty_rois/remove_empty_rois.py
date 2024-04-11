import numpy as np
import pandas as pd


def remove_empty_rois(signals_df: pd.DataFrame, std_threshold: float):
    """Takes a dataframe with the signals of each ROI and filters out the ROIs that don't contain a cell by checking the
     standard variation of that cell."""

    # calculate the standard deviation of each ROI signal
    stds = signals_df.std()

    # find ROIs above threshold
    above_thresh = stds >= std_threshold

    # Select ROIs above the threshold from the dataframe
    filtered_signals = signals_df.loc[:, above_thresh]
    filtered_rois = np.array(filtered_signals.columns)

    removed_rois = np.array(signals_df.loc[:, ~above_thresh].columns)

    return filtered_signals, filtered_rois, removed_rois
