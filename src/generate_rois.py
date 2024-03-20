import os
import shutil
import warnings

import numpy as np
from roifile import ImagejRoi, ROI_TYPE, ROI_OPTIONS

from src.utils.Dimensions import Dimensions
from src.utils.roi_names import roi_indexes_to_compact_label, roi_indexes_to_filename


def generate_rois_from_size(img_dims: Dimensions, roi_dims: Dimensions) -> dict:
    """Generates the ROIs for an image with ROI width and height as input"""

    # calculate number of ROIs
    n_horizontal = img_dims.width / roi_dims.width
    n_vertical = img_dims.height / roi_dims.height

    # show warning if image isn't divided without remainder by the specified width and height
    if not n_horizontal.is_integer():
        warnings.warn(
            f"The image with width {img_dims.width} can't be divided without remainder with the specified ROI width of {roi_dims.width}. The remainder is {img_dims.width % roi_dims.width} pixels")
    if not n_vertical.is_integer():
        warnings.warn(
            f"The image with height {img_dims.height} can't be divided without remainder with the specified ROI height of {roi_dims.height}.  The remainder is {img_dims.height % roi_dims.height} pixels")

    # floor the number of ROIs
    n_horizontal = int(n_horizontal)
    n_vertical = int(n_vertical)

    # create an array of ROIs
    rois = np.zeros((n_horizontal, n_vertical), dtype=ImagejRoi)

    for x in range(0, n_horizontal):
        for y in range(0, n_vertical):
            # we specify the upper left and lower right corners of the rectangle
            x_ul = x * roi_dims.width  # upper left x
            y_ul = y * roi_dims.height  # upper left y
            x_lr = x_ul + roi_dims.width - 1  # lower right x
            y_lr = y_ul + roi_dims.height - 1  # lower right y

            roi = ImagejRoi.frompoints(np.array([[x_ul, y_ul], [x_lr, y_lr]]))
            roi.roitype = ROI_TYPE.RECT
            roi.name = roi_indexes_to_compact_label(x, y)
            roi.options |= ROI_OPTIONS.OVERLAY_LABELS
            roi.options |= ROI_OPTIONS.SHOW_LABELS

            rois[x, y] = roi

    return {"n_horizontal": n_horizontal, "n_vertical": n_vertical, "rois": rois}


def save_rois(rois: np.array(ImagejRoi), save_dir: str) -> None:
    # create a directory for ROIs
    rois_dir = os.path.join(save_dir, 'ROIs')
    if os.path.exists(rois_dir):
        shutil.rmtree(rois_dir)
    os.mkdir(rois_dir)

    # loop through ROIs and save
    n_horizontal, n_vertical = rois.shape

    # we want the number of digits for each number to be the same as the maximum number of digits for readability
    max_digits = max(len(str(n_horizontal)), len(str(n_vertical)))

    for x in range(0, n_horizontal):
        for y in range(0, n_vertical):
            file_name = roi_indexes_to_filename(x, y, max_digits)
            file_path = os.path.join(rois_dir, file_name)
            rois[x, y].tofile(file_path)

    shutil.make_archive(os.path.join(save_dir, 'ROIs'), 'zip', rois_dir)  # zip the folder
    shutil.rmtree(rois_dir)  # remove the non-zipped directory
