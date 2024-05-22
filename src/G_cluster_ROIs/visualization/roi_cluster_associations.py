import numpy as np
from src.utils.ROI import ROI
from src.utils.coordinate_system import Dimensions

from matplotlib import pyplot as plt
import matplotlib.patches as patches

from src.utils.visualization.generate_distinct_colors import generate_distinct_colors
from src.utils.visualization.make_roi_axis_ticks import make_roi_axis_ticks
from src.utils.visualization.roi_rectangle_and_text import roi_rectangle_and_text
from src.utils.decorators import message_and_time


@message_and_time('')
def visualize_roi_cluster_associations(roi_clusters_dict, n_clusters: int, img_dims: Dimensions,
                                       removed_rois: np.array) -> plt.figure:
    """Generates a figure that shows which cluster each ROI belongs to.

    :param roi_clusters_dict : A dict with a key for each ROI and the value being the cluster it belongs to.
    :param n_clusters : Specify the number of clusters that should be computed. This should be the number of cells
    :param img_dims : A Dimensions object with the width and height of the image.
    :param removed_rois : An array containing all ROIs that were removed because they don't contain cells and are not
    clustered
     """
    colors = generate_distinct_colors(n_clusters)

    # ### plot each ROI as a rectangle with the color of the cluster ###
    fig, ax = plt.subplots(figsize=(40, 30))

    make_roi_axis_ticks('both', ax, img_dims)

    # plot filtered ROIs (ROIs on a cell)
    for roi, cluster in roi_clusters_dict.items():
        roi_rectangle_and_text(roi, ax,
                               {'linewidth': 0.1, 'edgecolor': 'black', 'facecolor': colors[cluster]},
                               str(cluster), {'fontsize': ROI.WIDTH_PIXELS // 2})

    # plot empty ROIs
    for roi in removed_rois:
        roi_rectangle_and_text(roi, ax,
                               {'linewidth': 0.1, 'edgecolor': 'grey', 'facecolor': 'black'}
                               )

    # manipulate figure properties
    ax.set_aspect('equal')
    ax.set_xlim(0, img_dims.width)
    ax.set_ylim(0, img_dims.height)
    plt.gca().invert_yaxis()

    # create legend
    legend_images = [patches.Patch(edgecolor='grey', facecolor='black')]
    legend_labels = ['empty']

    for cluster in range(n_clusters):
        legend_images.append(patches.Patch(edgecolor='black', facecolor=colors[cluster]))
        legend_labels.append(f'cl. {cluster}')

    return fig
