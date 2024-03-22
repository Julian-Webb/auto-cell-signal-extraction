import pandas as pd
import matplotlib.pyplot as plt


def single_plot(csv_path):
    df = pd.read_csv(csv_path)

    # plotting
    fig = plt.figure(figsize=(15, 15))

    for col in df.columns:
        # plot it if not all values are 0
        if not (df[col] == 0).all():
            plt.plot(df[col], label=col)

    plt.xlabel('Frame')
    plt.ylabel('Mean of ROI')
    plt.legend()

    return fig

