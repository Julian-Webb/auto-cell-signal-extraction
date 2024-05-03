import numpy as np
from matplotlib import pyplot as plt
from tifffile import TiffFile

from src.utils.ROI import ROI
from src.utils.coordinate_system import Dimensions


def rois_on_image(image_path: str, image_dims: Dimensions, colormap='plasma', grid_line_color='yellow',
                  frame_idx=0) -> plt.figure:
    # --- get the correct frame of the image ---
    with TiffFile(image_path) as tif:
        image = tif.pages[frame_idx].asarray()

    # --- show the image ---
    fig, ax = plt.subplots(figsize=(40, 30))
    ax.imshow(image,
              cmap=colormap,
              aspect='equal')

    # --- plot ROIs on top of image ---
    ax = make_ticks('x', ax, ROI.WIDTH, image_dims.width)
    ax = make_ticks('y', ax, ROI.HEIGHT, image_dims.height)

    minor_line_width = 1 if (ROI.WIDTH > 32 or ROI.HEIGHT > 32) else 0.5
    ax.grid(visible=True, which='major', linewidth=1, color=grid_line_color, linestyle=':')
    ax.grid(visible=True, which='minor', linewidth=minor_line_width, color=grid_line_color, linestyle=':')

    return fig


def make_ticks(dim: str, axis: plt.axis, roi_size, image_size, nth_major_tick: int = 8):
    major_ticks = np.arange(0, image_size, roi_size * nth_major_tick)
    major_labels = major_ticks // roi_size
    major_labels = [str(i) for i in major_labels]

    minor_ticks = np.arange(0, image_size, roi_size)
    minor_labels = minor_ticks // roi_size
    minor_labels = [str(i) for i in minor_labels]

    if dim == 'x':
        axis.set_xticks(major_ticks, major_labels, minor=False, rotation='vertical')
        axis.set_xticks(minor_ticks, minor_labels, minor=True, rotation='vertical')
    elif dim == 'y':
        axis.set_yticks(major_ticks, major_labels, minor=False)
        axis.set_yticks(minor_ticks, minor_labels, minor=True)

    return axis
