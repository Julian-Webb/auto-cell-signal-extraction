import os
import shutil
import numpy as np
import src.analysis_options as ao
from src.utils.ROI import ROI


def save_imagej_rois(rois: np.array) -> None:
    """Save the generated ROIs as a zip with .roi files which ImageJ/Fiji can use."""
    # create a directory for ROIs
    if os.path.exists(ao.rois_zip_folder_name):
        shutil.rmtree(ao.rois_zip_folder_name)
    os.mkdir(ao.rois_zip_folder_name)

    for x in range(0, ROI.N_HORIZONTAL):
        for y in range(0, ROI.N_VERTICAL):
            roi = rois[x, y]
            file_path = os.path.join(ao.rois_zip_folder_name, roi.filename())
            roi.as_ImagejRoi().tofile(file_path)  # save as imagej_roi

    shutil.make_archive(ao.rois_zip_folder_name, 'zip', ao.rois_zip_folder_name)  # zip the folder
    shutil.rmtree(ao.rois_zip_folder_name)  # remove the non-zipped directory
