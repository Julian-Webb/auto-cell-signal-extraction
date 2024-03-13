import skimage
import imagej
import os

# image paths
data_dir = '/Users/julian/development/PycharmProjects/glioblastoma/data/01_raw/'

single_image_path = os.path.join(data_dir, 'single_image', 'single_image.tiff')
single_image_rois_path = os.path.join(data_dir, 'single_image', 'ROIs.zip')
single_image_results_path = os.path.join(data_dir, 'single_image', 'Results.csv')

high_res_path = os.path.join(data_dir, 'high_res_test_stack', 'high_res_test_stack.tif')
real_image_path = os.path.join(data_dir, '276_AZD3965_Mathieu', '276_AZD3965_Mathieu.TIF')


def create_csv_from_rois(image_path: str, rois_path: str, results_path: str):
    """Generates the signals for each ROI based on the ROIs and an image"""

    image_name = os.path.split(image_path)[-1]

    # the macro
    open_rois_and_generate = f"""
    open("{image_path}");
    selectImage("{image_name}");
    open("{rois_path}");
    roiManager("Open", "{rois_path}");
    roiManager("Deselect");
    roiManager("Sort");
    roiManager("Show All");
    roiManager("Multi Measure");
    saveAs("Results", "{results_path}");
    """

    ij = imagej.init('sc.fiji:fiji')

    # open image
    jimage = ij.io().open(image_path)
    # convert image
    image = ij.py.from_java(jimage)

    # convert to imageplus, so we can use it
    image_plus = ij.py.to_imageplus(image)
    image_plus.setTitle(image_name)
    image_plus.show()

    # make sure there is an active window/image
    assert ij.WindowManager.getImage(image_name) is not None

    # run macro
    ij.py.run_macro(open_rois_and_generate)


create_csv_from_rois(single_image_path, single_image_rois_path, single_image_results_path)
