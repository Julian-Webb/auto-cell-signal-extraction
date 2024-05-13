import numpy as np
import pandas as pd
import src.options as opt


def save_repr_signals(repr_signals: np.array, repr_rois, n_clusters: int) -> None:
    labels = [f'Cluster {i}' for i in range(n_clusters)]

    rois_df = pd.DataFrame(repr_rois.reshape(1, -1), columns=labels, index=['Representative ROI'])

    # we transpose because we want each column to represent one cluster
    signals_df = pd.DataFrame(repr_signals.T, columns=labels)

    df = pd.concat([rois_df, signals_df])
    df.to_csv(opt.H_signal_per_cluster_csv_path)
