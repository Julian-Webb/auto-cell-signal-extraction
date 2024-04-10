import numpy as np
from matplotlib import patches, pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib import colors

from src.utils.coordinate_system import Dimensions
from src.utils.ROI import ROI


def plot_roi_stds(signals_arr: np.array, rois: np.array, img_dims: Dimensions, std_threshold: float):
    """Plots the standard deviation of each ROI signal"""

    cmap = plt.colormaps['seismic']

    stds = signals_arr.std(axis=2)

    # normalize stds between 0 and 1
    # we use a TwoSlopeNorm to center the threshold
    norm = colors.TwoSlopeNorm(vmin=stds.min(), vcenter=std_threshold, vmax=stds.max())
    scalar_mappable = ScalarMappable(norm, cmap)

    normalized_stds = scalar_mappable.to_rgba(stds)

    fig, ax = plt.subplots()
    for roi in rois.flatten():
        facecolor = normalized_stds[roi.x_idx, roi.y_idx, :]

        # draw rectangle
        upper_left, _ = roi.coordinates()
        rect = patches.Rectangle((upper_left.x, upper_left.y), ROI.WIDTH, ROI.HEIGHT,
                                 linewidth=0.1, edgecolor='black', facecolor=facecolor)
        ax.add_patch(rect)

    # manipulate figure properties
    ax.set_aspect('equal')

    ax.set_xlim(0, img_dims.width)
    ax.set_ylim(0, img_dims.height)

    plt.gca().invert_yaxis()

    ax.set_xlabel('horizontal pixels')
    ax.set_ylabel('vertical pixels')

    # create colorbar
    colorbar = fig.colorbar(scalar_mappable, ax=ax)
    # colorbar.ax.axhline(std_threshold, color='black', label='threshold')  # marks the threshold

    # fig.tight_layout()

    return fig
