import pandas as pd
from matplotlib import pyplot as plt


def presentation_grid_plot(signals_df: pd.DataFrame) -> plt.figure:
    # fig, axs = plt.subplots(nrows=ROI.N_VERTICAL, ncols=ROI.N_HORIZONTAL, sharex=True, sharey=True)
    fig, axs = plt.subplots(nrows=5, ncols=5, sharex=True, sharey=True)

    for roi in signals_df.columns:
        ax = axs[roi.y_idx - 4, roi.x_idx - 4]

        ax.plot(signals_df[roi])

        # Remove ticks and labels from x and y axes
        ax.set_xticks([])
        ax.set_yticks([])

        # Hide grid lines
        ax.grid(False)

        # make vertical labels only for the very left
        if roi.x_idx-4 == 0:
            ax.set_ylabel(roi.y_idx, rotation=0, fontsize=8)

        # make horizontal labels only on the bottom
        ax.xaxis.set_label_position('top')
        if roi.y_idx-4 == 0:
            ax.set_xlabel(roi.x_idx, fontsize=8)

    fig.tight_layout()
    # make space between subplots very small
    plt.subplots_adjust(hspace=0.01, wspace=0.01)
    return fig