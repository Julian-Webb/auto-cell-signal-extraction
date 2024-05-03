import numpy as np
from matplotlib import pyplot as plt


def plot_cluster_signals(cluster_signals: np.array):
    """Plots the representative signals of each cluster."""

    n_clusters = cluster_signals.shape[0]
    fig = plt.figure()

    for i in range(n_clusters):
        plt.plot(cluster_signals[i, :], label=f'cluster {i}')

    plt.legend()
    plt.xlabel('Frame')
    plt.ylabel('Signal Value')

    if n_clusters <= 15:
        plt.tight_layout()
    return fig
