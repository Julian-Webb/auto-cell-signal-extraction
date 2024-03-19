import numpy as np
from matplotlib import pyplot as plt


def plot_representative_signals(repr_signals: np.array):
    """Takes in an array """

    n_clusters = repr_signals.shape[0]
    fig = plt.figure(figsize=(15, 15))

    for i in range(n_clusters):
        plt.plot(repr_signals[i, :], label=f'cluster {i}')

    plt.legend()

    return fig
