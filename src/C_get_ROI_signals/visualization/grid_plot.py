import numpy as np
from matplotlib import pyplot as plt

from src.utils.ROI import ROI


def grid_plot(signals_arr: np.array) -> plt.figure:
    # NOTE: this function is pretty fragile. Don't expect too much

    fig, ax = plt.subplots(nrows=ROI.N_VERTICAL, ncols=ROI.N_HORIZONTAL, sharex=True, sharey=True)

    for x in range(ROI.N_HORIZONTAL):
        for y in range(ROI.N_VERTICAL):
            cur_axis = ax[y, x]
            cur_axis.plot(signals_arr[x, y, :])

            # Remove ticks and labels from x and y axes
            cur_axis.set_xticks([])
            cur_axis.set_yticks([])

            # Hide grid lines
            cur_axis.grid(False)

            # make vertical labels only for the very left
            if x == 0:
                cur_axis.set_ylabel(y, rotation=0, fontsize=8)

            # make horizontal labels only on the bottom
            cur_axis.xaxis.set_label_position('top')
            if y == 0:
                cur_axis.set_xlabel(x, fontsize=8)

    # fig.tight_layout()
    # make space between subplots very small
    plt.subplots_adjust(hspace=0.01, wspace=0.01)
    return fig
