import numpy as np


def compute_representative_signal(clusters: list, signals_arr: np.array):
    """This function merges the signals belonging to one cluster of ROIs into one signal.
    It takes in a list where the indexes are clusters and the sub-lists are the ROIs that are contained in that cluster.
    It selects the signal with the highest amplitude for each cluster.
    It outputs a single signal for each cluster/cell."""

    n_clusters = len(clusters)
    n_frames = signals_arr.shape[2]

    # the signals for each cluster
    cluster_signals = np.zeros((n_clusters, n_frames))

    for cluster_idx, rois in enumerate(clusters):
        # ### select signal with the highest amplitude for each cluster. ####

        # select the signals in this cluster
        xs = np.array(rois)[:, 0]  # the x-indexes of the ROIs
        ys = np.array(rois)[:, 1]  # the y-indexes of the ROIs
        signals = signals_arr[xs, ys, :]

        # select/create a representative signal
        repr_signal = max_amplitude_signal(signals)

        cluster_signals[cluster_idx, :] = repr_signal

    return cluster_signals


def max_amplitude_signal(signals: np.array):
    # get the index of the maximum overall value
    arg_max = np.unravel_index(signals.argmax(), signals.shape)

    # select the signal which contains the overall maximum value
    max_signal = signals[arg_max[0], :]
    return max_signal
