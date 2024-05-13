import matplotlib.pyplot as plt
from matplotlib import patches
from src.utils.ROI import ROI


def roi_rectangle_and_text(roi: ROI, axes: plt.Axes, rectangle_kwargs: dict = None, cluster_label: str = None,
                           label_kwargs: dict = None
                           ):
    """Plot a rectangle and a label with the cluster number on the given axes.
    :param roi: The ROI to plot.
    :param axes: The axes to plot on.
    :param rectangle_kwargs: Keyword arguments for the rectangle patch.
        Example:
        `{linewidth: 0.1,
         edgecolor:'black',
         facecolor: colors[cluster],
         alpha: 0.4}`
    :param cluster_label: The label to plot in the center of the rectangle. Typically, the cluster number.
    :param label_kwargs: Keyword arguments for the label.
        Example:
        `{fontsize=ROI.WIDTH // 2,
         alpha=0.8}`
    """
    if rectangle_kwargs is None:
        rectangle_kwargs = {'linewidth': 0.1,
                            'edgecolor': 'black',
                            'facecolor': 'transparent',
                            'alpha': 1}

    upper_left, _ = roi.coordinates()  # upper left corner of the ROI
    rect = patches.Rectangle((upper_left.x, upper_left.y),
                             ROI.WIDTH, ROI.HEIGHT,
                             **rectangle_kwargs)
    axes.add_patch(rect)

    if cluster_label is not None:
        center = roi.center()
        axes.text(center.x, center.y,
                  cluster_label,
                  ha='center', va='center',
                  **label_kwargs
                  )

    return axes
