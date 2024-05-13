import numpy as np
import pandas as pd
import src.options as opt


def save_repr_signals(repr_signals: np.array, n_clusters: int) -> None:
    labels = [f'Cluster {i}' for i in range(n_clusters)]
    # we transpose because we want each column to represent one cluster
    df = pd.DataFrame(repr_signals.T, columns=labels)
    df.to_csv(opt.H_signal_per_cluster_csv_path)
