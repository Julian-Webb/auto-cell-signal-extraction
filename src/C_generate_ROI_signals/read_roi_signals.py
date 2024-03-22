import numpy as np
import pandas as pd
import tifffile as tf

from src.utils.ROI import ROI


def read_roi_signals(image_path: str, n_frames: int, rois: np.array, pixel_dtype) -> np.array:
    """Takes a multi-image tiff and extracts the signals of each ROI.
    Returns dataframe with the signals for each ROI, as well as an array which holds the same data.
    The array indexes correspond to [roi.x_idx, roi.y_idx, frame]"""

    # imread returns the image with the following shape: (n_frames, vertical dim, horizontal dim)
    img = tf.imread(image_path)

    # we make a signals array and a signals dataframe which store the same data but in a different format
    # signals_arr = np.zeros((ROI.N_HORIZONTAL, ROI.N_VERTICAL, n_frames), dtype=pixel_dtype)
    signals_arr = np.zeros(shape=(ROI.N_HORIZONTAL, ROI.N_VERTICAL, n_frames))
    signals_df = pd.DataFrame()

    # loop through each roi
    for roi in rois.flatten():
        # get the index ranges for setting the signals
        ul, lr = roi.coordinates()  # get the upper left and lower right corners
        x_left = ul.x
        y_top = ul.y
        x_right = lr.x + 1  # we add 1 because indexing is exclusive
        y_bottom = lr.y + 1

        roi_cutout = img[:, y_top: y_bottom, x_left: x_right]

        # we want to get the mean of all pixel values for each frame
        roi_signal = np.mean(roi_cutout, axis=(1, 2))

        signals_df[roi.compact_label()] = roi_signal
        signals_arr[roi.x_idx, roi.y_idx, :] = roi_signal

    return signals_arr, signals_df
