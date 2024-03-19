import os

from matplotlib import pyplot as plt
import matplotlib.patches as patches
import colorsys


def visualize_roi_cluster_associations(roi_clusters_dict, n_clusters: int, roi_dims: tuple[int, int],
                       img_dims: tuple[int, int]) -> plt.figure:
    """Generates a figure that shows which cluster each ROI belongs to.

    Parameters:
     roi_clusters_dict : A dict with a key for each ROI and the value being the cluster it belongs to.
     roi_dims : the x and y dimensions of a ROI.
     """
    colors = generate_distinct_colors(n_clusters)

    # plot each ROI as a rectangle with the color of the cluster
    fig, ax = plt.subplots()

    width, height = roi_dims
    for roi, cluster in roi_clusters_dict.items():
        roi_x, roi_y = roi
        x = roi_x * width
        y = roi_y * height

        rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='black', facecolor=colors[cluster])
        ax.add_patch(rect)

        # ax.text(x + 0.5 * width, y + 0.5 * height, str(cluster), ha='center', va='center')

        continue

    # manipulate figure properties
    ax.set_aspect('equal')

    ax.set_xlim(0, img_dims[0])
    ax.set_ylim(0, img_dims[1])

    plt.gca().invert_yaxis()

    ax.set_xlabel('horizontal pixels')
    ax.set_ylabel('vertical pixels')

    # create legend
    custom_legend = []
    for cluster in range(n_clusters):
        custom_legend.append(patches.Patch(edgecolor='black', facecolor=colors[cluster]))
    ax.legend(custom_legend, list(range(0, n_clusters)), bbox_to_anchor=(1, 1))

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

