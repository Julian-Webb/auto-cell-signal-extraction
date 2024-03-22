import pandas as pd
from matplotlib import pyplot as plt

from src.utils.ROI import ROI


def grid_plot(csv_path) -> plt.figure:
    # NOTE: this function is pretty fragile. Don't expect too much

    df = pd.read_csv(csv_path)

    fig, ax = plt.subplots(nrows=ROI.N_VERTICAL, ncols=ROI.N_HORIZONTAL, sharex=True, sharey=True)

    for x in range(ROI.N_HORIZONTAL):
        for y in range(ROI.N_VERTICAL):
            col_name = f'Mean(({x}; {y}))'
            cur_axis = ax[y, x]
            cur_axis.plot(df[col_name])

            # Remove ticks and labels from x and y axes
            cur_axis.set_xticks([])
            cur_axis.set_yticks([])

            # Hide grid lines
            cur_axis.grid(False)

    return fig
