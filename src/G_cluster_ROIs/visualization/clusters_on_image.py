import numpy as np
from matplotlib import pyplot as plt
from tifffile import TiffFile

from src.utils.ROI import ROI
from src.utils.coordinate_system import Dimensions
from src.utils.visualization.generate_distinct_colors import generate_distinct_colors
from src.utils.visualization.make_roi_axis_ticks import make_roi_axis_ticks
from src.utils.visualization.roi_rectangle_and_text import roi_rectangle_and_text
from src.utils.decorators import message_and_time


@message_and_time('')
def clusters_on_image(roi_clusters_dict: dict, representative_rois: np.array, n_clusters: int, image_path: str,
                      image_dims: Dimensions, colormap='grey', frame_idx: int = 0):
    # --- get the correct frame of the image ---
    with TiffFile(image_path) as tif:
        image = tif.pages[frame_idx].asarray()

    # --- show the image ---
    fig, ax = plt.subplots(figsize=(40, 30))

    make_roi_axis_ticks('both', ax, image_dims)

    ax.imshow(image,
              cmap=colormap,
              aspect='equal')

    # --- plot ROIs on top of image ---
    colors = generate_distinct_colors(n_clusters)

    for roi, cluster in roi_clusters_dict.items():
        # check if it's a representative ROI
        if roi in representative_rois:
            inverse_color = [1 - c for c in colors[cluster]]
            roi_rectangle_and_text(roi, ax,
                                   {'linewidth': 0.3, 'edgecolor': inverse_color, 'facecolor': colors[cluster],
                                    'alpha': 0.5},
                                   str(cluster),
                                   {'fontsize': ROI.WIDTH // 2, 'weight': 'bold', 'alpha': 0.8, 'color': inverse_color})
        else:
            roi_rectangle_and_text(roi, ax,
                                   {'linewidth': 0.1, 'edgecolor': 'black', 'facecolor': colors[cluster],
                                    'alpha': 0.5},
                                   str(cluster),
                                   {'fontsize': ROI.WIDTH // 2, 'alpha': 0.8})

    return fig
