import numpy as np
from matplotlib import pyplot as plt

from src.utils.ROI import ROI
from src.utils.coordinate_system import Dimensions


def make_roi_axis_ticks(dim: str, axis: plt.axis, image_dims: Dimensions, nth_major_tick: int = 8) -> plt.axis:
    """
    Adds ticks to the axis for the ROI indices.
    :param dim: 'x', 'y', or 'both'
    :param axis:
    :param image_dims:
    :param nth_major_tick: Every n-th tick will be a major tick. Specify n here.
    :return: The axis with the ticks added.
    """

    if dim == 'x':
        image_size = image_dims.width
        roi_size = ROI.WIDTH
    elif dim == 'y':
        image_size = image_dims.height
        roi_size = ROI.HEIGHT
    elif dim == 'both':
        axis = make_roi_axis_ticks('x', axis, image_dims, nth_major_tick)
        axis = make_roi_axis_ticks('y', axis, image_dims, nth_major_tick)
        return axis
    else:
        raise ValueError(f"dim must be 'x', 'y', or 'both'. Got {dim}.")

    major_ticks = np.arange(0, image_size, roi_size * nth_major_tick)
    major_labels = major_ticks // roi_size
    major_labels = [str(i) for i in major_labels]

    minor_ticks = np.arange(0, image_size, roi_size)
    minor_labels = minor_ticks // roi_size
    minor_labels = [str(i) for i in minor_labels]

    if dim == 'x':
        axis.set_xticks(major_ticks, major_labels, minor=False, rotation='vertical')
        axis.set_xticks(minor_ticks, minor_labels, minor=True, rotation='vertical')
        axis.set_xlabel('ROI x index')
        # Move x-axis to the top
        axis.xaxis.tick_top()
        axis.xaxis.set_label_position('top')
    elif dim == 'y':
        axis.set_yticks(major_ticks, major_labels, minor=False)
        axis.set_yticks(minor_ticks, minor_labels, minor=True)
        axis.set_ylabel('ROI y index')

    return axis
