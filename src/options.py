# This file contains the options for the analysis
import os
from src.utils.ROI import ROI

# %% ---------------------------------------- Dataset Options ----------------------------------------------------------
# TODO specify base directory here
base_dir = '/Users/julian/development/PycharmProjects/auto_signal_extraction'

test_stack = {'dir': os.path.join(base_dir, 'data', 'high_res_test_stack'),
              'name': os.path.join('raw', 'high_res_test_stack.tif'),
              'rolling_window_size': 4,
              'std_threshold': 20,
              'n_cells': 4,
              'max_cell_size_pixels': 450,
              'pixels_per_mm': 795.46,
              }

D_233_MG_B1 = {'dir': os.path.join(base_dir, 'data', '233_MG_B1'),
               'name': os.path.join('raw', '233_MG_B1_STACK.tif'),
               'rolling_window_size': 80,
               'std_threshold': 6,
               'n_cells': 9,
               'max_cell_size_pixels': 450,
               'pixels_per_mm': 795.46,
               }

D_233_MG_B2 = {'dir': os.path.join(base_dir, 'data', '233_MG_B2'),
               'name': os.path.join('raw', '233_MG_B2_STACK.tif'),
               'rolling_window_size': 80,
               'std_threshold': 6,
               'n_cells': 9,
               'max_cell_size_pixels': 450,
               'pixels_per_mm': 795.46,
               }

D_276_AZD3965_Mathieu = {'dir': os.path.join(base_dir, 'data', '276_AZD3965_Mathieu'),
                         'name': os.path.join('raw', '276_AZD3965_Mathieu.TIF'),
                         'std_threshold': 16,
                         'rolling_window_size': 100,
                         'n_cells': 429,
                         'max_cell_size_pixels': 450,
                         'pixels_per_mm': 795.46,
                         }

D_233_NoMG_A1 = {'dir': os.path.join(base_dir, 'data', '233_NoMG_A1'),
                 'name': os.path.join('raw', '233_NoMG_A1_STACK.tif'),
                 'std_threshold': 15,
                 'rolling_window_size': 80,
                 'n_cells': 95,
                 'max_cell_size_pixels': 100,
                 'pixels_per_mm': 795.46,
                 }

cutout = {'dir': os.path.join(base_dir, 'data', '233_NoMG_A1_cutout'),
          'name': os.path.join('raw', '233_NoMG_A1_STACK_cutout.tif'),
          'std_threshold': 15,
          'rolling_window_size': 60,
          'n_cells': 13,
          'max_cell_size_pixels': 30,
          'pixels_per_mm': 795.46,
          }

tiny_cutout = {'dir': os.path.join(base_dir, 'data', 'tiny_cutout'),
               'name': os.path.join('raw', 'tiny_cutout.tif'),
               'std_threshold': 15,
               'rolling_window_size': 60,
               'n_cells': 5,
               'max_cell_size_pixels': 30,
               'pixels_per_mm': 795.46,
               }

single_cell = {'dir': os.path.join(base_dir, 'data', 'single_cell'),
               'name': os.path.join('raw', 'single_cell.tif'),
               'std_threshold': 15,
               'rolling_window_size': 60,
               'n_cells': 1,
               'max_cell_size_pixels': 30,
               'pixels_per_mm': 795.46,
               }

# %% ---------------------------------------- Analysis Options ---------------------------------------------------------
# 1: Path Names
# Please specify the image name the directory where the image is stored
dataset_info = test_stack
directory = dataset_info['dir']
image_name = dataset_info['name']
image_path = os.path.join(directory, image_name)

# 0: Specify numerical analysis values
# Specify the sizes of your ROIs in pixels. The value should be a whole number (no decimal point)
ROI.WIDTH_PIXELS = ROI.HEIGHT_PIXELS = 128

# The number of pixels per millimeter in the calcium image
ROI.PIXELS_PER_MM = dataset_info['pixels_per_mm']

# C: Specify ROI signal summary statistic #
# This is how the signal of the ROI will be generated based on the value of each pixel it contains.
roi_signal_summary_statistic: str = 'max'
assert roi_signal_summary_statistic in ['mean', 'max']

# D: The size of the rolling window in frames. Used to calculate the rolling mean for detrending the signal
rolling_window_size: int = dataset_info['rolling_window_size']

# E: The threshold of standard deviation for removing empty ROIs.
# Any ROIs with a std below this threshold will be filtered out.
std_threshold: float = dataset_info['std_threshold']

# F: Specify the largest diameter of any cell in the image.
# This will be used to determine within which area signal comparisons between ROIs should be made.
# NOTE: you might want to specify a size that is slightly larger (~10%) than the largest diameter to be sure.
F_spatial_comparison_range_pixels = dataset_info['max_cell_size_pixels']

# G: Specify clustering method
clustering_method: str = 'spatial_weighted_kmeans'
assert clustering_method in ['basic_kmeans', 'spatial_weighted_kmeans', 'agglomerative']

if clustering_method in ['basic_kmeans', 'spatial_weighted_kmeans']:
    # How much the spatial location vs. the signal of the ROIs should be taken into account when clustering.
    # If >1, location will be weighted more heavily. If <1, signals will be weighted more heavily.
    spatial_weight: float = 2.5
    k_clusters: int = dataset_info['n_cells']
elif clustering_method == 'agglomerative':
    # Specify the maximum amount of clusters to be generated. This should be the number of the cells in the recording
    max_clusters: int = dataset_info['n_cells']

# 2: Plot and File Options
# Specify which plots and files to generate. This influences the time to execute.
all_on: bool = False  # Turn all options on or off
intense_options: bool = False
most_useful: bool = True

B_save_imagej_rois: bool = all_on or False  # *
B_plot_rois_on_image: bool = all_on or most_useful or False

C_create_all_ROI_signals_file: bool = intense_options or all_on or False  # *
C_generate_ROI_signals_grid_plot: bool = intense_options or all_on  # *
C_generate_ROI_signals_single_plot: bool = intense_options or all_on  # *

D_create_detrended_signals_file: bool = intense_options or all_on or False  # *
D_generate_detrended_signals_grid_plot: bool = intense_options or all_on  # *
D_generate_detrended_signals_single_plot: bool = intense_options or all_on  # *
E_create_filtered_ROI_signals_file: bool = all_on or False
E_plot_ROI_stds_on_image: bool = all_on or most_useful or False

F_create_ROI_distances_file: bool = all_on or False

G_plot_clusters_on_image: bool = all_on or True
G_plot_ROI_cluster_associations: bool = all_on or False
G_plot_dendrogram: bool = all_on or True

H_plot_clusters_and_representative_rois_on_image: bool = all_on or most_useful or True
H_plot_signals_per_cluster: bool = all_on or False
H_generate_cluster_signals_video: bool = all_on or intense_options  # *

# * : high impact on performance. Set to False unless needed

# %% ------------------------------------ File & Path Names ------------------------------------------------------------
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

G_clusters_on_image_path = os.path.join(figures_dir, 'G_clusters_on_image.png')
G_roi_cluster_associations_path = os.path.join(figures_dir, 'G_ROI-cluster_associations.png')
G_dendrogram_path = os.path.join(figures_dir, 'G_dendrogram.png')

H_clusters_on_image_path = os.path.join(figures_dir, 'H_highlighted_clusters_on_image.png')
H_signal_per_cluster_plot_path = os.path.join(figures_dir, 'H_signal_per_cluster.png')
H_signal_per_cluster_csv_path = os.path.join(results_dir, 'H_signal_per_cluster.csv')
H_cluster_signals_video_path = os.path.join(figures_dir, 'H_cluster_signals_video.tif')
