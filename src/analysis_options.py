# This file contains the options for the analysis
import os
from src.utils.ROI import ROI

# ############# For testing ###############
base_dir = '/Users/julian/development/PycharmProjects/glioblastoma'

test_stack = {'dir': os.path.join(base_dir, 'data', 'high_res_test_stack'),
              'name': os.path.join('raw', 'high_res_test_stack.tif'),
              'std_threshold': 20
              }

calcium_img = {'dir': os.path.join(base_dir, 'data', '276_AZD3965_Mathieu'),
               'name': os.path.join('raw', '276_AZD3965_Mathieu.TIF'),
               'std_threshold': 9,
               }

# single image
# single_image_dir = '/Users/julian/development/PycharmProjects/glioblastoma/data/01_raw/single_image/'
# single_image_path = os.path.join(single_image_dir, 'single_image.tiff')
# #########################################
# 1: Path Names
# Please specify the image name the directory where the image is stored
data_dict = calcium_img
directory = data_dict['dir']
image_name = data_dict['name']
image_path = os.path.join(directory, image_name)

# 0: Specify numerical analysis values
# Specify the sizes of your ROIs in pixels. The value should be a whole number (no decimal point)
# ROI.WIDTH = 2048 // 4
# ROI.HEIGHT = 1536 // 3

ROI.WIDTH = ROI.HEIGHT = 64

# The threshold of standard deviation for removing empty ROIs.
# Any ROIs with a std below this threshold will be filtered out.
std_threshold = data_dict['std_threshold']


# 2: Plots
# Specify which plots to generate. This influences the time to execute.
intense_options = False

generate_ROI_stds_plot = True
generate_ROI_signals_grid_plot = intense_options  # *
generate_ROI_signals_single_plot = intense_options  # *
generate_ROI_cluster_associations_plot = True
generate_dendrogram = True
generate_signals_per_cluster_plot = True
generate_cluster_signals_video = intense_options  # *
# * : high impact on performance. Set to False unless needed

# ################################## FILE & PATH NAMES #################################################################
# make figures directory
figures_dir = os.path.join(directory, 'figures')
if not os.path.exists(figures_dir):
    os.mkdir(figures_dir)

# make results directory
results_dir = os.path.join(directory, 'results')
if not os.path.exists(results_dir):
    os.mkdir(results_dir)

rois_zip_folder_name = os.path.join(results_dir, 'B_ROIs')  # the .zip will be appended automatically
roi_signals_csv_path = os.path.join(results_dir, 'C_ROI_signals.csv')
roi_signals_grid_plot_path = os.path.join(figures_dir, 'C_ROI_signals_grid_plot.png')
roi_signals_single_plot_path = os.path.join(figures_dir, 'C_ROI_signals_single_plot.png')
roi_stds_plot_path = os.path.join(figures_dir, 'D_ROI_stds')
filtered_roi_signals_csv_path = os.path.join(results_dir, 'D_filtered_ROI_signals.csv')
roi_distances_csv_path = os.path.join(results_dir, 'E_ROI_distance_matrix.csv')
roi_cluster_associations_path = os.path.join(figures_dir, 'F_ROI-cluster_associations.png')
dendrogram_path = os.path.join(figures_dir, 'F_dendrogram.png')
signal_per_cluster_plot_path = os.path.join(figures_dir, 'G_signal_per_cluster.png')
signal_per_cluster_csv_path = os.path.join(results_dir, 'G_signal_per_cluster.csv')
cluster_signals_video_path = os.path.join(figures_dir, 'G_cluster_signals_video.tif')
