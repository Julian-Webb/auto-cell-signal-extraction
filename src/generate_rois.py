import os
import shutil
import warnings

import numpy as np
from roifile import ImagejRoi, ROI_TYPE, ROI_OPTIONS
from PIL import Image


def generate_rois_from_size(image_path: str, roi_width: int, roi_height: int) -> dict:
    """Generates the ROIs for an image with ROI width and height as input"""

    # calculate number of ROIs
    with Image.open(image_path) as image:
        n_horizontal = image.width / roi_width
        n_vertical = image.height / roi_height

        # show warning if image isn't divided without remainder by the specified width and height
        if not n_horizontal.is_integer():
            warnings.warn(
                f"The image with width {image.width} can't be divided without remainder with the specified ROI width of {roi_width}. The remainder is {image.width % roi_width} pixels")
        if not n_vertical.is_integer():
            warnings.warn(
                f"The image with height {image.height} can't be divided without remainder with the specified ROI height of {roi_height}.  The remainder is {image.height % roi_height} pixels")

    # floor the number of ROIs
    n_horizontal = int(n_horizontal)
    n_vertical = int(n_vertical)

    # create an array of ROIs
    rois = np.zeros((n_horizontal, n_vertical), dtype=ImagejRoi)

    for x in range(0, n_horizontal):
        for y in range(0, n_vertical):
            # we specify the upper left and lower right corners of the rectangle
            x_ul = x * roi_width  # upper left x
            y_ul = y * roi_height  # upper left y
            x_lr = x_ul + roi_width - 1  # lower right x
            y_lr = y_ul + roi_height - 1  # lower right y

            roi = ImagejRoi.frompoints(np.array([[x_ul, y_ul], [x_lr, y_lr]]))
            roi.roitype = ROI_TYPE.RECT
            roi.name = f'({x}; {y})'
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
            x_formatted = f'{x:0{max_digits}d}'
            y_formatted = f'{y:0{max_digits}d}'
            file_name = f'ROI_x{x_formatted}_y{y_formatted}.roi'
            file_path = os.path.join(rois_dir, file_name)
            rois[x, y].tofile(file_path)

    shutil.make_archive(os.path.join(save_dir, 'ROIs'), 'zip', rois_dir)  # zip the folder
    shutil.rmtree(rois_dir)  # remove the non-zipped directory
