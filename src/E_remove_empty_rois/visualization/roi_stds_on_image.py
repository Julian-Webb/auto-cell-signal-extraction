import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib import colors
from tifffile import TiffFile

from src.utils.ROI import ROI
from src.utils.coordinate_system import Dimensions
from src.utils.visualization.make_roi_axis_ticks import make_roi_axis_ticks
from src.utils.visualization.roi_rectangle_and_text import roi_rectangle_and_text


def plot_roi_stds_on_image(signals_df: pd.DataFrame, img_dims: Dimensions,
                           std_threshold: float, image_path: str, frame_idx: int = 0,
                           filtered_rois: np.array = None,
                           removed_rois: np.array = None) -> plt.figure():
    """
    Plots the standard deviation of each ROI signal on top of the image.
    :param signals_df:
    :param img_dims:
    :param std_threshold:
    :param image_path:
    :param frame_idx: The frame of the calcium image that should be plotted
    :param filtered_rois: The ROIs that were kept after filtering. If specified, these will be marked with a dot.
    :param removed_rois: The ROIs that were removed because they were empty. If specified, these will be marked.
    :return:
    """

    fig, ax = plt.subplots(figsize=(img_dims.width // 50, img_dims.height // 50))

    make_roi_axis_ticks('both', ax, img_dims)

    # --- plot image ---
    if image_path is not None:
        with TiffFile(image_path) as tif:
            image = tif.pages[frame_idx].asarray()
        ax.imshow(image, cmap='gray', aspect='equal')

    # --- plot STDs ---
    cmap = plt.colormaps['seismic']

    stds = signals_df.std()

    # normalize stds between 0 and 1
    # we use a TwoSlopeNorm to center the threshold
    min_std = stds.min()
    max_std = stds.max()
    if std_threshold < min_std:
        raise ValueError(
            f'The std_threshold ({std_threshold}) for removing ROIs is smaller than the minimum standard deviation of the ROI signals ({min_std}).')
    if std_threshold > max_std:
        raise ValueError(
            f'The std_threshold ({std_threshold}) for removing ROIs is larger than the maximum standard deviation of the ROI signals ({min_std}).')
    norm = colors.TwoSlopeNorm(vmin=min_std, vcenter=std_threshold, vmax=max_std)
    scalar_mappable = ScalarMappable(norm, cmap)

    normalized_stds = scalar_mappable.to_rgba(stds)

    # --- Draw Rectangles for each ROI STD ---
    for i, roi in enumerate(signals_df.columns):  # iterate over all ROIs
        facecolor = normalized_stds[i, :]

        roi_rectangle_and_text(roi, ax, {'linewidth': 0.1, 'edgecolor': 'black', 'facecolor': facecolor, 'alpha': 0.5})

    # --- Draw dots over filtered ROIs that were kept ---
    marker_size = ROI.WIDTH * ROI.HEIGHT // 50
    if filtered_rois is not None:
        filtered_coords = np.zeros(shape=(2, filtered_rois.size))  # coordinates of the filtered ROIs
        for i, roi in enumerate(filtered_rois):
            center = roi.center()
            filtered_coords[:, i] = center.x, center.y
        # For some reason, this makes white space at the right and bottom axis
        ax.scatter(filtered_coords[0], filtered_coords[1], marker='o', color='green', s=marker_size, alpha=0.5)

    # --- Draw dots over removed ROIs ---
    if removed_rois is not None:
        removed_coords = np.zeros(shape=(2, removed_rois.size))  # coordinates of the removed ROIs
        for i, roi in enumerate(removed_rois):
            center = roi.center()
            removed_coords[:, i] = center.x, center.y
        ax.scatter(removed_coords[0], removed_coords[1], marker='o', color='black', s=marker_size, alpha=0.5)

    # --- manipulate figure properties ---
    ax.set_aspect('equal')

    ax.set_xlim(0, img_dims.width)
    ax.set_ylim(0, img_dims.height)

    plt.gca().invert_yaxis()

    # create colorbar
    colorbar = fig.colorbar(scalar_mappable, ax=ax)
    # colorbar.ax.axhline(std_threshold, color='black', label='threshold')  # marks the threshold
    colorbar.set_label('Standard Deviation')
    return fig
