from matplotlib import pyplot as plt
from tifffile import TiffFile
from src.utils.ROI import ROI
from src.utils.coordinate_system import Dimensions
from src.utils.visualization.make_roi_axis_ticks import make_roi_axis_ticks
from src.utils.decorators import message_and_time


@message_and_time('')
def rois_on_image(image_path: str, image_dims: Dimensions, colormap='gray', grid_line_color='yellow',
                  frame_idx=0) -> plt.figure:
    # --- get the correct frame of the image ---
    with TiffFile(image_path) as tif:
        image = tif.pages[frame_idx].asarray()

    # --- show the image ---
    fig, ax = plt.subplots(figsize=(image_dims.width // 50, image_dims.height // 50))
    ax.imshow(image,
              cmap=colormap,
              aspect='equal')

    # --- plot ROIs on top of image ---
    ax = make_roi_axis_ticks('both', ax, image_dims)

    minor_line_width = 1 if (ROI.WIDTH_PIXELS > 32 or ROI.HEIGHT_PIXELS > 32) else 0.5
    ax.grid(visible=True, which='major', linewidth=1, color=grid_line_color, linestyle=':')
    ax.grid(visible=True, which='minor', linewidth=minor_line_width, color=grid_line_color, linestyle=':')

    ax.set_xlabel('ROI x index')
    ax.set_ylabel('ROI y index')

    return fig
