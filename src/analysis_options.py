# This file contains the options for the analysis
import os
from src.utils.ROI import ROI

# ############# For testing ###############
base_dir = '/Users/julian/development/PycharmProjects/glioblastoma'

test_stack = {'dir': os.path.join(base_dir, 'data', 'high_res_test_stack'),
              'name': os.path.join('raw', 'high_res_test_stack.tif'),
              'rolling_window_size': 4,
              'std_threshold': 20,
              'n_cells': 4,
              'max_cell_size_pixels': 450,
              }

D_233_MG_B1 = {'dir': os.path.join(base_dir, 'data', '233_MG_B1'),
               'name': os.path.join('raw', '233_MG_B1_STACK.tif'),
               'rolling_window_size': 80,
               'std_threshold': 6,
               'n_cells': 9,
               'max_cell_size_pixels': 450,
               }

D_233_MG_B2 = {'dir': os.path.join(base_dir, 'data', '233_MG_B2'),
               'name': os.path.join('raw', '233_MG_B2_STACK.tif'),
               'rolling_window_size': 80,
               'std_threshold': 6,
               'n_cells': 9,
               'max_cell_size_pixels': 450,
               }

D_276_AZD3965_Mathieu = {'dir': os.path.join(base_dir, 'data', '276_AZD3965_Mathieu'),
                         'name': os.path.join('raw', '276_AZD3965_Mathieu.TIF'),
                         'std_threshold': 16,
                         'rolling_window_size': 100,
                         'n_cells': 429,
                         'max_cell_size_pixels': 450,
                         }

D_233_NoMG_A1 = {'dir': os.path.join(base_dir, 'data', '233_NoMG_A1'),
                 'name': os.path.join('raw', '233_NoMG_A1_STACK.tif'),
                 'std_threshold': 14,
                 'rolling_window_size': 80,
                 'n_cells': 95,
                 'max_cell_size_pixels': 450,
                 }

# #########################################
# 1: Path Names
# Please specify the image name the directory where the image is stored
dataset_info = test_stack
directory = dataset_info['dir']
image_name = dataset_info['name']
image_path = os.path.join(directory, image_name)

# 0: Specify numerical analysis values
# Specify the sizes of your ROIs in pixels. The value should be a whole number (no decimal point)
# ROI.WIDTH = 2048 // 4
# ROI.HEIGHT = 1536 // 3

# ROI.WIDTH = 4
# ROI.HEIGHT = 4

ROI.WIDTH = ROI.HEIGHT = 128

# The size of the rolling window in frames. Used to calculate the rolling mean for detrending the signal
rolling_window_size: int = dataset_info['rolling_window_size']

# Specify ROI signal summary statistic #
# This is how the signal of the ROI will be generated based on the value of each pixel it contains.
roi_signal_summary_statistic: str = 'max'  # should be 'mean' or 'max'

# The threshold of standard deviation for removing empty ROIs.
# Any ROIs with a std below this threshold will be filtered out.
std_threshold: float = dataset_info['std_threshold']

# Specify the largest diameter of any cell in the image.
# This will be used to determine within which area signal comparisons between ROIs should be made.
# NOTE: you might want to specify a size that is slightly larger (~10%) than the largest diameter to be sure.
F_max_cell_size_pixels = dataset_info['max_cell_size_pixels']

# Specify the maximum amount of clusters to be generated. This should be the number of the cells in the recording.
max_clusters: int = dataset_info['n_cells']

# 2: Plot and File Options
# Specify which plots and files to generate. This influences the time to execute.
intense_options: bool = True

B_save_imagej_rois = True  # *
B_plot_rois_on_image = True

C_create_all_ROI_signals_file = intense_options  # *
C_generate_ROI_signals_grid_plot = intense_options  # *
C_generate_ROI_signals_single_plot = intense_options  # *

D_create_detrended_signals_file = intense_options  # *
D_generate_detrended_signals_grid_plot = intense_options  # *
D_generate_detrended_signals_single_plot = intense_options  # *

E_create_filtered_ROI_signals_file = True
E_generate_ROI_stds_plot = True

F_create_ROI_distances_file = True

G_generate_ROI_cluster_associations_plot = True
G_generate_dendrogram = True
H_generate_signals_per_cluster_plot = True
H_generate_cluster_signals_video = intense_options  # *
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

B_rois_zip_folder_name = os.path.join(results_dir, 'B_ROIs')  # the .zip will be appended automatically
B_plot_rois_on_image_path = os.path.join(figures_dir, 'B_ROIs_on_image.png')

C_roi_signals_csv_path = os.path.join(results_dir, 'C_raw_ROI_signals.csv')
C_roi_signals_grid_plot_path = os.path.join(figures_dir, 'C_raw_signals_grid_plot.png')
C_roi_signals_single_plot_path = os.path.join(figures_dir, 'C_raw_signals_single_plot.png')

D_detrended_signals_csv_path = os.path.join(results_dir, 'D_detrended_ROI_signals.csv')
D_detrended_signals_single_plot_path = os.path.join(figures_dir, 'D_detrended_signals_single_plot.png')
D_detrended_signals_grid_plot_path = os.path.join(figures_dir, 'D_detrended_signals_grid_plot.png')

E_roi_stds_plot_path = os.path.join(figures_dir, 'E_ROI_stds')
E_filtered_roi_signals_csv_path = os.path.join(results_dir, 'E_filtered_ROI_signals.csv')

F_roi_distances_csv_path = os.path.join(results_dir, 'F_ROI_distance_matrix.csv')

G_roi_cluster_associations_path = os.path.join(figures_dir, 'G_ROI-cluster_associations.png')
G_dendrogram_path = os.path.join(figures_dir, 'G_dendrogram.png')

H_signal_per_cluster_plot_path = os.path.join(figures_dir, 'H_signal_per_cluster.png')
H_signal_per_cluster_csv_path = os.path.join(results_dir, 'H_signal_per_cluster.csv')
H_cluster_signals_video_path = os.path.join(figures_dir, 'H_cluster_signals_video.tif')
