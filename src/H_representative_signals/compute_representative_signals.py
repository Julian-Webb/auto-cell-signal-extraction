import numpy as np
import pandas as pd

from src.utils.ROI import ROI

from src.utils.decorators import message_and_time


@message_and_time('')
def compute_representative_signals(clusters: dict, signals_df: pd.DataFrame, n_clusters: int,
                                   n_frames: int) -> (np.array, np.array):
    """
    Computes a representative signal for each cluster. This is based on the signal with the highest maximum value.
    :param clusters: A dict containing a list of the ROIs (values) belonging to each cluster (keys).
    :param signals_df:
    :param n_clusters:
    :param n_frames:
    :return: A `np.array` with the signals of each cluster and a `np.array` with the representative ROIs.
    """
    # the representative ROIs and their signals for each cluster
    repr_signals = np.zeros((n_clusters, n_frames),
                            dtype=signals_df.dtypes.iloc[0])
    repr_rois = np.zeros(n_clusters, dtype=ROI)

    # for each cluster, find the signal with the highest maximum value
    for cluster_idx, rois in clusters.items():
        signals = signals_df[rois]  # select the signals in this cluster
        repr_signals[cluster_idx, :], repr_rois[cluster_idx] = max_amplitude_signal(signals)

    return repr_signals, repr_rois


def max_amplitude_signal(signals: pd.DataFrame):
    # Get the maximum signal of the absolute values
    max_per_roi = signals.abs().max()
    max_roi = max_per_roi.idxmax()
    max_signal = signals[max_roi]
    return max_signal, max_roi
