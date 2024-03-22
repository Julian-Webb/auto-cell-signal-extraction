import os
import shutil
import numpy as np

from src.utils.ROI import ROI


def save_imagej_rois(rois: np.array, save_dir: str) -> None:
    """Save the generated ROIs as a zip with .roi files which ImageJ/Fiji can use."""
    # create a directory for ROIs
    rois_dir = os.path.join(save_dir, 'ROIs')
    if os.path.exists(rois_dir):
        shutil.rmtree(rois_dir)
    os.mkdir(rois_dir)

    for x in range(0, ROI.N_HORIZONTAL):
        for y in range(0, ROI.N_VERTICAL):
            roi = rois[x, y]
            file_path = os.path.join(rois_dir, roi.filename())
            roi.as_ImagejRoi().tofile(file_path)  # save as imagej_roi

    shutil.make_archive(os.path.join(save_dir, 'ROIs'), 'zip', rois_dir)  # zip the folder
    shutil.rmtree(rois_dir)  # remove the non-zipped directory
