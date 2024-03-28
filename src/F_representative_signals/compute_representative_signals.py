import numpy as np
import pandas as pd


def compute_representative_signals(clusters: dict, signals_df: pd.DataFrame, n_clusters: int, n_frames: int) -> np.array:
    """This function merges the signals belonging to one cluster of ROIs into one signal.
    It takes in a list where the indexes are clusters and the sub-lists are the ROIs that are contained in that cluster.
    It selects the signal with the highest amplitude for each cluster.
    It outputs a single signal for each cluster/cell."""

    # the signals for each cluster
    repr_signals = np.zeros((n_clusters, n_frames))

    for cluster_idx, rois in clusters.items():
        # ### select signal with the highest amplitude for each cluster. ####
        # get the labels for all rois in this cluster
        labels = [roi for roi in rois]

        # select the signals in this cluster
        signals = signals_df[labels].values

        # select/create a representative signal
        repr_signal = max_amplitude_signal(signals)

        repr_signals[cluster_idx, :] = repr_signal

    return repr_signals


def max_amplitude_signal(signals: np.array):
    # get the index of the maximum overall value
    arg_max = np.unravel_index(signals.argmax(), signals.shape)

    # select the signal which contains the overall maximum value
    max_signal = signals[:, arg_max[1]]
    return max_signal
