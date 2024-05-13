import pandas as pd
import matplotlib.pyplot as plt

from src.utils.decorators import message_and_time


@message_and_time('')
def single_plot(signals_df: pd.DataFrame):

    # plotting
    fig = plt.figure()

    for col in signals_df.columns:
        # plot it if not all values are 0
        if not (signals_df[col] == 0).all():
            plt.plot(signals_df[col], linewidth=0.5, label=col)

    plt.xlabel('Frame')
    plt.ylabel('ROI signal')
    plt.legend(loc='upper right')
    plt.tight_layout()
    return fig

