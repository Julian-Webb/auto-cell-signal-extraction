import numpy as np
import pandas as pd


def remove_empty_rois(signals_df: pd.DataFrame, std_threshold: float):
    """Takes a dataframe with the signals of each ROI and filters out the ROIs that don't contain a cell by checking the
     standard variation of that cell."""

    # calculate the standard deviation of each ROI signal
    stds = signals_df.std()

    # find values below threshold
    filtered_rois = []
    removed_rois = []

    # remove the ROIs below the threshold from the dataframe
    for roi in signals_df.columns:
        if stds[roi] < std_threshold:
            signals_df.drop(roi, axis='columns', inplace=True)
            removed_rois.append(roi)
        else:
            filtered_rois.append(roi)

    # return the filtered dataframe
    filtered_rois = np.array(filtered_rois)
    removed_rois = np.array(removed_rois)
    return signals_df, filtered_rois, removed_rois
