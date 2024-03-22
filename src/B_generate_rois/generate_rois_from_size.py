import warnings
from typing import Any

import numpy as np

from src.utils.coordinate_system import Dimensions
from src.utils.ROI import ROI


def generate_rois_from_size(img_dims: Dimensions) -> np.ndarray[Any, np.dtype[ROI]]:
    """Generates the ROIs for an image with ROI width and height as input"""

    # calculate number of ROIs
    n_horizontal = img_dims.width / ROI.WIDTH
    n_vertical = img_dims.height / ROI.HEIGHT

    # show warning if image isn't divided without remainder by the specified width and height
    if not n_horizontal.is_integer():
        warnings.warn(
            f"The image with width {img_dims.width} can't be divided without remainder with the specified ROI width of \
            {ROI.WIDTH}. The remainder is {img_dims.width % ROI.WIDTH} pixels")
    if not n_vertical.is_integer():
        warnings.warn(
            f"The image with height {img_dims.height} can't be divided without remainder with the specified ROI height \
            of {ROI.HEIGHT}.  The remainder is {img_dims.height % ROI.HEIGHT} pixels")

    # floor the number of ROIs
    ROI.N_HORIZONTAL = int(n_horizontal)
    ROI.N_VERTICAL = int(n_vertical)
    del n_horizontal, n_vertical

    # create an array of ROIs
    rois = np.zeros((ROI.N_HORIZONTAL, ROI.N_VERTICAL), dtype=ROI)
    for x in range(ROI.N_HORIZONTAL):
        for y in range(ROI.N_VERTICAL):
            rois[x, y] = ROI(x, y)

    return rois

