import numpy as np
from matplotlib import pyplot as plt


def plot_repr_signals(repr_signals: np.array):
    """Takes in an array """

    n_clusters = repr_signals.shape[0]
    # fig = plt.figure(figsize=(15, 15))
    fig = plt.figure()

    for i in range(n_clusters):
        plt.plot(repr_signals[i, :], label=f'cluster {i}')

    plt.legend()
    plt.xlabel('Frame')
    plt.ylabel('Signal Value')

    plt.tight_layout()
    return fig
