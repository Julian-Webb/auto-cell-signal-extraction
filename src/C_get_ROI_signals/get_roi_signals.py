import numpy as np
import pandas as pd
import tifffile as tf

from src.utils.ROI import ROI
from src.utils.SignalSummaryStatistics import SignalSummaryStatistics

from src.utils.decorators import message_and_time


@message_and_time('')
def get_roi_signals(image_path: str, n_frames: int, rois: np.array,
                    summary_statistic: SignalSummaryStatistics) -> np.array:
    """Takes a multi-image tiff and extracts the signals of each ROI. For each frame, it takes the mean of the values
    in the ROI.
    Returns dataframe with the signals for each ROI, as well as an array which holds the same data.
    The array indexes correspond to [roi.x_idx, roi.y_idx, frame]
    """

    if summary_statistic == SignalSummaryStatistics.MEAN:
        get_signal_func = _mean_signal
    elif summary_statistic == SignalSummaryStatistics.MAX:
        get_signal_func = _max_signal
    else:
        raise ValueError(f'summary_statistic should be either MEAN or MAX but is {summary_statistic}')

    # imread returns the image with the following shape: (n_frames, vertical dim, horizontal dim)
    img = tf.imread(image_path)

    # we make a signals array and a signals dataframe which store the same data but in a different format
    signals_arr = np.zeros(shape=(ROI.N_HORIZONTAL, ROI.N_VERTICAL, n_frames))

    indexes = [i for i in range(n_frames)]
    signals_df = pd.DataFrame(columns=rois.flatten(), index=indexes)

    # loop through each roi
    for roi in rois.flatten():
        # get the index ranges for setting the signals
        ul, lr = roi.corners_pixels()  # get the upper left and lower right corners
        x_left = ul.x
        y_top = ul.y
        x_right = lr.x + 1  # we add 1 because indexing is exclusive
        y_bottom = lr.y + 1

        roi_cutout = img[:, y_top: y_bottom, x_left: x_right]

        # get the signal for this cutout
        roi_signal = get_signal_func(roi_cutout)

        signals_df[roi] = roi_signal
        signals_arr[roi.x_idx, roi.y_idx, :] = roi_signal

    return signals_arr, signals_df


def _mean_signal(roi_cutout):
    # we want to get the mean of all pixel values for each frame
    return np.mean(roi_cutout, axis=(1, 2))


def _max_signal(roi_cutout):
    # get the maximum value in the ROI
    argmax = np.unravel_index(roi_cutout.argmax(), roi_cutout.shape)

    # Now we take the signal of the pixel with the maximum value for all frames
    return roi_cutout[:, argmax[1], argmax[2]]
