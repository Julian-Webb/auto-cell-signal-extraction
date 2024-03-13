import pandas as pd
import matplotlib.pyplot as plt


def single_plot(csv_path):
    df = pd.read_csv(csv_path)

    # plotting
    plt.figure(figsize=(30, 20))

    for col in df.columns:
        plt.plot(df[col], label=col)

    plt.xlabel('Frame')
    plt.ylabel('Mean of ROI')
    plt.legend()
    plt.show()


def ordered_subplots(csv_path, n_horizontal, n_vertical) -> plt.figure:
    # NOTE: this function is pretty fragile. Don't expect too much

    df = pd.read_csv(csv_path)

    fig, ax = plt.subplots(nrows=n_vertical, ncols=n_horizontal, sharex=True, sharey=True)

    for x in range(n_horizontal):
        for y in range(n_vertical):
            col_name = f'Mean(({x}; {y}))'
            cur_axis = ax[y, x]
            cur_axis.plot(df[col_name])

            # Remove ticks and labels from x and y axes
            cur_axis.set_xticks([])
            cur_axis.set_yticks([])

            # Hide grid lines
            cur_axis.grid(False)

            # cur_axis.set_title(f'ROI {x}, {y}')

    return fig
