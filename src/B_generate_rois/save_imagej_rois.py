import os
import shutil
import numpy as np
import src.options as opt
from src.utils.ROI import ROI
from src.utils.decorators import message_and_time


@message_and_time('')
def save_imagej_rois(rois: np.array) -> None:
    """Save the generated ROIs as a zip with .roi files which ImageJ/Fiji can use."""
    # create a directory for ROIs
    if os.path.exists(opt.B_rois_zip_folder_name):
        shutil.rmtree(opt.B_rois_zip_folder_name)
    os.mkdir(opt.B_rois_zip_folder_name)

    for x in range(0, ROI.N_HORIZONTAL):
        for y in range(0, ROI.N_VERTICAL):
            roi = rois[x, y]
            file_path = os.path.join(opt.B_rois_zip_folder_name, roi.filename())
            roi.as_ImagejRoi().tofile(file_path)  # save as imagej_roi

    shutil.make_archive(opt.B_rois_zip_folder_name, 'zip', opt.B_rois_zip_folder_name)  # zip the folder
    shutil.rmtree(opt.B_rois_zip_folder_name)  # remove the non-zipped directory
