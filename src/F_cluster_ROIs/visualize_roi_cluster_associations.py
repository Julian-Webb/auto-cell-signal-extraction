import numpy as np
from src.utils.ROI import ROI
from src.utils.coordinate_system import Dimensions

from matplotlib import pyplot as plt
import matplotlib.patches as patches
import colorsys


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
    fig, ax = plt.subplots()

    # plot filtered ROIs (ROIs on a cell)
    for roi, cluster in roi_clusters_dict.items():
        upper_left, _ = roi.coordinates()

        rect = patches.Rectangle((upper_left.x, upper_left.y), ROI.WIDTH, ROI.HEIGHT,
                                 linewidth=0.1, edgecolor='black', facecolor=colors[cluster])

        ax.add_patch(rect)

        # ax.text(x + 0.5 * ROI.WIDTH, y + 0.5 * ROI.HEIGHT, str(cluster), ha='center', va='center')

    # plot empty ROIs
    for roi in removed_rois:
        upper_left, _ = roi.coordinates()
        rect = patches.Rectangle((upper_left.x, upper_left.y), ROI.WIDTH, ROI.HEIGHT,
                                 linewidth=0.1, edgecolor='grey', facecolor='black')
        ax.add_patch(rect)

    # manipulate figure properties
    ax.set_aspect('equal')

    ax.set_xlim(0, img_dims.width)
    ax.set_ylim(0, img_dims.height)

    plt.gca().invert_yaxis()

    ax.set_xlabel('horizontal pixels')
    ax.set_ylabel('vertical pixels')

    # create legend
    legend_images = [patches.Patch(edgecolor='grey', facecolor='black')]
    legend_labels = ['empty']

    for cluster in range(n_clusters):
        legend_images.append(patches.Patch(edgecolor='black', facecolor=colors[cluster]))
        legend_labels.append(f'cl. {cluster}')
    ax.legend(legend_images, legend_labels, bbox_to_anchor=(1, 1))

    if n_clusters <= 16:
        fig.tight_layout()

    return fig


def generate_distinct_colors(n):
    # Generate evenly spaced hues in the color spectrum
    hues = [i / n for i in range(n)]

    # Convert hues to RGB
    colors = []
    for hue in hues:
        r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.8)  # You can adjust saturation and value as needed
        colors.append((r, g, b))

    return colors
