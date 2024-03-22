# This file contains the options for the analysis
import os

# ############# For testing ###############
base_dir = '/Users/julian/development/PycharmProjects/glioblastoma'

test_stack = {'dir': os.path.join(base_dir, 'data', '01_raw', 'high_res_test_stack'), 'name': 'high_res_test_stack.tif'}

calcium_img = {'dir': os.path.join(base_dir, 'data', '01_raw', '276_AZD3965_Mathieu'),
               'name': '276_AZD3965_Mathieu.TIF'}

# single image
# single_image_dir = '/Users/julian/development/PycharmProjects/glioblastoma/data/01_raw/single_image/'
# single_image_path = os.path.join(single_image_dir, 'single_image.tiff')
# #########################################

# 0: Path Names
# Please specify the image name the directory where the image is stored
directory = test_stack['dir']
image_name = test_stack['name']
image_path = os.path.join(directory, image_name)

# 1: ROI Sizes
# Specify the sizes of your ROIs in pixels. The value should be a whole number (no decimal point)
roi_width = 2048 // 4
roi_height = 1536 // 3

# roi_width = 8
# roi_height = 8

# 2: Plots
# Specify which plots to generate. This influences the time to execute.
generate_ROI_signals_grid_plot = False
generate_ROI_signals_single_plot = True
generate_ROI_cluster_associations_plot = True
generate_signals_per_cluster_plot = True
generate_cluster_signals_video = True

# ################################## DEVELOPER OPTIONS #################################################################
#  Don't touch these unless you know what you're doing!
ask_user_to_confirm_ROI_signals_were_generated = False  # This should always be True except for testing

# make figures directory
figures_dir = os.path.join(directory, 'figures')
if not os.path.exists(figures_dir):
    os.mkdir(figures_dir)
