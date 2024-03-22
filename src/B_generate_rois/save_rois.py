import numpy as np
import os
import shutil
from roifile import ImagejRoi

from src.utils.roi_names import roi_indexes_to_filename


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
