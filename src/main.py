import os
import time

import analysis_options as ao
from src.A_load_image_data.load_image_data import load_image_data
from src.C_generate_ROI_signals.read_roi_signals import read_roi_signals
from src.utils.ROI import ROI
from src.B_generate_rois.generate_rois_from_size import generate_rois_from_size
from src.B_generate_rois.save_imagej_rois import save_imagej_rois
from src.C_generate_ROI_signals.with_imagej.remove_first_column import remove_first_csv_column
from src.C_generate_ROI_signals.with_imagej.convert_csv_to_array import convert_csv_to_array
from src.C_generate_ROI_signals.visualization.single_plot import single_plot
from src.C_generate_ROI_signals.visualization.grid_plot import grid_plot
from src.D_calculate_similarity.distance_adjusted_similarity import distance_adjusted_similarity
from src.E_cluster_ROIs.cluster_rois import cluster_rois
from src.E_cluster_ROIs.visualize_roi_cluster_associations import visualize_roi_cluster_associations
from src.F_representative_signals.compute_representative_signals import compute_representative_signals
from src.F_representative_signals.visualization.representative_signals_video import representative_signals_video
from src.F_representative_signals.visualization.plot_representative_signals import plot_representative_signals

timing = {}
initial_time = time.time()
#
#
# ##### Step 0.0: Initialization ##################################################################################


#
#
# ##### Step 1: Load the image data ####################################################################################
start_time = time.time()

n_frames, img_dims, pixel_dtype = load_image_data(ao.image_path)

timing['Step 1'] = time.time() - start_time
#
#
# ##### Step 2: Compute the regions of interest (ROIs) #################################################################
#
start_time = time.time()

rois = generate_rois_from_size(img_dims)
save_imagej_rois(rois, ao.directory)

print(f"\nA grid of {ROI.N_HORIZONTAL} x {ROI.N_VERTICAL} (horizontal x vertical) ROIs has been created.\n")

timing['Step 2'] = time.time() - start_time
print(f"Step 2 (computing ROIs) : {timing['Step 2']:.1f} seconds\n")
#
#
# ##### Step 3: Generate the signals based on the ROIs #################################################################
#
start_time = time.time()

# # The user needs to do this manually with Fiji
# print('Please manually perform the following steps now:')
# print('1. Drag the image and the ROIs into Fiji.')
# print('2. Open the ROI Manager, go to "More" and click "Sort". The ROIs should get sorted')
# print('3. Then go to "More" and click "Multi Measure". Enable "Measure all x slices" and "One row per slice".\
#  Then click ok')
# print('4. A results window should open. Save it as "Results.csv"')
#
# if ao.ask_user_to_confirm_ROI_signals_were_generated:
#     ans = ''
#     while ans != 'yes':
#         ans = input('If you have performed all the above steps, please type "yes" and press Enter: ')
#
# # remove the first column from the .csv because it represents the frame which isn't necessary
csv_path = os.path.join(ao.directory, 'Results.csv')
# remove_first_csv_column(csv_path)
#
# signals_arr = convert_csv_to_array(csv_path)

roi_signals_path = os.path.join(ao.directory, 'ROI_signals.csv')
signals_arr, signals_df = read_roi_signals(ao.image_path, n_frames, rois, pixel_dtype)
signals_df.to_csv(roi_signals_path)

if ao.generate_ROI_signals_grid_plot:
    fig = grid_plot(csv_path)
    fig.savefig(os.path.join(ao.figures_dir, 'ROI_signals_grid_plot.png'))
    del fig

if ao.generate_ROI_signals_single_plot:
    fig = single_plot(csv_path)
    fig.savefig(os.path.join(ao.figures_dir, 'ROI_signals_single_plot.png'))
    del fig

timing['Step 3'] = time.time() - start_time
print(f"Step 3 (computing ROI signals with FIJI) : {timing['Step 3']:.1f} seconds\n")
#
#
# ##### Step 4: Compute the similarity of the ROIs #####################################################################
#
start_time = time.time()
print('Computing distance-adjusted similarity matrix...', end='')

# We calculate the distance-adjust signal similarity for each pair of ROIs
dist_adj_sim = distance_adjusted_similarity(signals_arr, ROI.N_HORIZONTAL, ROI.N_VERTICAL)
dist_adj_sim.to_csv(os.path.join(ao.directory, 'Distance-adjusted similarity.csv'))

print('Done')
timing['Step 4'] = time.time() - start_time
print(f"Step 4 (computing similarity) : {timing['Step 4']:.1f} seconds\n")
#
#
# ##### Step 5: Create clusters based on similarity ####################################################################
#
start_time = time.time()
print('Creating clusters...', end='')

clusters, n_clusters, roi_clusters_dict = cluster_rois(dist_adj_sim, signals_arr, similarity_threshold=0.7,
                                                       n_horizontal=ROI.N_HORIZONTAL, n_vertical=ROI.N_VERTICAL,
                                                       n_frames=n_frames)

if ao.generate_ROI_cluster_associations_plot:
    fig = visualize_roi_cluster_associations(roi_clusters_dict, n_clusters, img_dims)
    fig.savefig(os.path.join(ao.figures_dir, 'ROI-cluster_associations.png'))
    del fig

print('Done')
timing['Step 5'] = time.time() - start_time
print(f"Step 5 (clustering) : {timing['Step 5']:.1f} seconds\n")
#
#
# ##### Step 6: Create/Select a representative signal for each cluster/cell and save the result ########################
#
start_time = time.time()

representative_signals = compute_representative_signals(clusters, signals_arr)

timing['Step 6'] = time.time() - start_time
print(f"Step 6 (computing representative signals) : {timing['Step 6']:.1f} seconds\n")

if ao.generate_signals_per_cluster_plot:
    fig = plot_representative_signals(representative_signals)
    fig.savefig(os.path.join(ao.figures_dir, 'signal_per_cluster.png'))
    del fig

# create video
start_time = time.time()

if ao.generate_cluster_signals_video:
    video_path = os.path.join(ao.figures_dir, 'cluster_signals_video.tif')
    representative_signals_video(video_path, roi_clusters_dict, representative_signals, n_frames, img_dims,
                                 pixel_dtype)

timing['video'] = time.time() - start_time
print(f"Step 7 (generating video) : {timing['video']:.1f} seconds\n")
########################################################################################################################
print(f"Elapsed time: {(time.time() - initial_time):.1f} seconds")
