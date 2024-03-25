import pandas as pd
import matplotlib.pyplot as plt


def single_plot(signals_df: pd.DataFrame):

    # plotting
    fig = plt.figure()

    for col in signals_df.columns:
        # plot it if not all values are 0
        if not (signals_df[col] == 0).all():
            plt.plot(signals_df[col], label=col)

    plt.xlabel('Frame')
    plt.ylabel('Mean of ROI')
    plt.legend()
    plt.tight_layout()
    return fig

