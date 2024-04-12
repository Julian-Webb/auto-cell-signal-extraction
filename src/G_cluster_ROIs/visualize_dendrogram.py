import numpy as np
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram


def visualize_dendrogram(clustering_steps: np.array, rois: np.array):
    roi_labels = np.array([str(roi) for roi in rois])
    fig = plt.figure()

    dendrogram(clustering_steps, labels=roi_labels)
    return fig
