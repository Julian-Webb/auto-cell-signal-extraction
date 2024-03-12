import os
import shutil

from roifile import ImagejRoi, ROI_TYPE, ROI_OPTIONS
import numpy as np


def roi_example():
    roi = ImagejRoi.frompoints(np.array([[1.1, 2.2], [3.3, 4.4], [5.5, 6.6]]))
    roi.roitype = ROI_TYPE.POINT
    roi.options |= ROI_OPTIONS.SHOW_LABELS

    # Export the instance to an ImageJ ROI formatted byte string or file:
    out = roi.tobytes()
    print(out[:4])
    roi.tofile('_test.roi')

    # Read the ImageJ ROI from the file and verify the content:
    roi2 = ImagejRoi.fromfile('_test.roi')
    print(roi2 == roi)
    print(roi.roitype == ROI_TYPE.POINT)
    print(roi.subpixelresolution)
    print(roi.coordinates())

    print(roi.left, roi.top, roi.right, roi.bottom)

    # Plot the ROI using matplotlib:
    roi.plot()

    # View the overlays stored in a ROI, ZIP, or TIFF file from a command line:
    # python -m roifile _test.roi


def test_generate_rois(data_dir: str, img_name: str):
    n_horizontal_rois = 4
    n_vertical_rois = 6

    # calculate dimensions of an ROI
    with Image.open(os.path.join(data_dir, img_name)) as image:
        roi_width = image.width / n_horizontal_rois
        roi_height = image.height / n_vertical_rois

    # create ROIs
    # Note: The first coordinate of a point represents the horizontal axis and the second represents the vertical axis
    roi1 = ImagejRoi.frompoints([[100, 100], [100, 300], [400, 300], [400, 100], [100, 100]])
    roi1.roitype = ROI_TYPE.RECT
    # roi1.stroke_color = b'\xff\xff\xff\x00'
    # roi1.position = 1

    roi2 = ImagejRoi.frompoints([[500, 500], [800, 700]])
    roi2.roitype = ROI_TYPE.RECT
    # roi2.stroke_color = b'\xff\xff\xff\x00'
    # roi2.position = 1

    roi3 = ImagejRoi.frompoints([[0, 0], [100, 100]])
    roi3.roitype = ROI_TYPE.RECT

    # create a directory for ROIs
    rois_dir = os.path.join(data_dir, 'ROIs')
    if not os.path.exists(rois_dir):
        os.mkdir(rois_dir)
    roi1.tofile(os.path.join(rois_dir, 'ROI_1.roi'))
    roi2.tofile(os.path.join(rois_dir, 'ROI_2.roi'))
    roi3.tofile(os.path.join(rois_dir, 'ROI_3.roi'))

    # zip the folder
    shutil.make_archive(os.path.join(data_dir, 'ROIs'), 'zip', rois_dir)
