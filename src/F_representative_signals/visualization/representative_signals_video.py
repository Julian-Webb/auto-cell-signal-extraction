from src.utils.ROI import ROI
from src.utils.coordinate_system import Dimensions

import numpy as np
import tifffile as tf
from tifffile import COMPRESSION


def representative_signals_video(video_path: str, roi_clusters_dict: dict, representative_signals: np.array,
                                 n_frames: int, img_dims: Dimensions, pixel_dtype: np.dtype):
    """Creates a multi-image tiff which shows the signal for each cluster and the cluster's location."""
    video_arr = compute_video_array(roi_clusters_dict, representative_signals, n_frames, img_dims, pixel_dtype)

    # save array as multi-image tiff
    # tf.imwrite(video_path, video_arr, compression='zlib', imagej=True)
    tf.imwrite(video_path, video_arr, imagej=True)

    return video_arr


def compute_video_array(roi_clusters_dict: dict, representative_signals: np.array, n_frames: int,
                        img_dims: Dimensions, pixel_dtype: np.dtype):
    """Computes an array which will be interpreted by tifffile as the tiff we want to generate"""

    # NOTE: tifffile has the following meaning for the dimensions of a multi-image tiff:
    # Dimension 0 -> frame
    # Dimension 1 -> vertical pixel index
    # Dimension 2 -> horizontal pixel index
    # This differs from the  rest of this project where dimension 1 represents horizontal and 2 represents vertical.

    # initialize array
    video_arr = np.zeros(shape=(n_frames, img_dims.height, img_dims.width), dtype=pixel_dtype)

    # We loop through each ROI and set its pixel values to the signal of the cluster with respect to the frame
    for roi, cluster in roi_clusters_dict.items():
        # get the signal values for this cluster for all frames
        signal_values = representative_signals[cluster, :]

        # determine ROI boundaries (the upper boundary is exclusive)
        x_left = roi[0] * ROI.WIDTH
        y_top = roi[1] * ROI.HEIGHT
        x_right = x_left + ROI.WIDTH
        y_bottom = y_top + ROI.HEIGHT

        # set the values of this ROI to the corresponding signal values for all frames.
        reshaped_signal_values = signal_values[:, None, None]
        video_arr[:, y_top:y_bottom, x_left:x_right] = reshaped_signal_values

    return video_arr
