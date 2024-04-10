import numpy as np
import pandas as pd
import src.analysis_options as ao


def save_repr_signals(repr_signals: np.array, n_clusters: int) -> None:
    labels = [f'Cluster {i}' for i in range(n_clusters)]
    # we transpose because we want each column to represent one cluster
    df = pd.DataFrame(repr_signals.T, columns=labels)
    df.to_csv(ao.signal_per_cluster_csv_path)
