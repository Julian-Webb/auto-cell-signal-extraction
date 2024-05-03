from matplotlib import pyplot as plt
from tifffile import TiffFile

from src.utils.ROI import ROI
from src.utils.coordinate_system import Dimensions
from src.utils.visualization.generate_distinct_colors import generate_distinct_colors
from src.utils.visualization.make_roi_axis_ticks import make_roi_axis_ticks
from src.utils.visualization.roi_rectangle_and_text import roi_rectangle_and_text


def clusters_on_image(roi_clusters_dict: dict, n_clusters: int, image_path: str, image_dims: Dimensions, colormap='grey', frame_idx: int = 0):
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
        roi_rectangle_and_text(roi, ax,
                               {'linewidth': 0.1, 'edgecolor': 'black', 'facecolor': colors[cluster],
                                'alpha': 0.5},
                               str(cluster),
                               {'fontsize': ROI.WIDTH // 2, 'alpha': 0.8})

    return fig
