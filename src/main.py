import os
import shutil
import time

import numpy as np
import tifffile as tf
import analysis_options as ao
from generate_rois import generate_rois_from_size, save_rois
from generate_signals import remove_first_csv_column, convert_csv_to_array
from src.distance_adjusted_similarity import distance_adjusted_similarity
from src.cluster_rois import cluster_rois
from src.merge_clustered_signals import compute_representative_signal
from src.utils.Dimensions import Dimensions
from src.utils.get_n_frames import get_n_frames
from src.visualization.cluster_signals_video import cluster_signals_video
from src.visualization.plot_representative_signals import plot_representative_signals
from src.visualization.plot_signals_from_csv import grid_plot, single_plot
from src.visualization.visualize_roi_cluster_associations import visualize_roi_cluster_associations

timing = {}
initial_time = time.time()
#
#
# ##### Step 0.0: Initialization ##################################################################################
# create ROI dimensions object based on specified dimensions
roi_dims = Dimensions(int(ao.roi_width), int(ao.roi_height))

#
#
# ##### Step 1: Load the image #########################################################################################
start_time = time.time()

with tf.TiffFile(ao.image_path) as image:
    n_frames = get_n_frames(image)

    # determine height and width
    img_dims = Dimensions(width=image.pages[0].shape[1], height=image.pages[0].shape[0])

    # determine datatype of pixel values (It needs to be the same for all frames!)
    pixel_dtype = image.asarray(key=0).dtype  # get the dtype for the first frame

    # determine the color map
    colormap = image.pages[0].colormap

timing['Step 1'] = time.time() - start_time
#
#
# ##### Step 2: Compute the regions of interest (ROIs) #################################################################
#
start_time = time.time()

rois_dict = generate_rois_from_size(img_dims, roi_dims)
save_rois(rois_dict["rois"], ao.directory)
n_horizontal, n_vertical = rois_dict["n_horizontal"], rois_dict["n_vertical"]
print(f"\nA grid of {n_horizontal} x {n_vertical} (horizontal x vertical) ROIs has been created.\n")

timing['Step 2'] = time.time() - start_time
print(f"Step 2 (computing ROIs) : {timing['Step 2']:.1f} seconds\n")
#
#
# ##### Step 3: Generate the signals based on the ROIs #################################################################
#
start_time = time.time()

# The user needs to do this manually with Fiji
print('Please manually perform the following steps now:')
print('1. Drag the image and the ROIs into Fiji.')
print('2. Open the ROI Manager, go to "More" and click "Sort". The ROIs should get sorted')
print('3. Then go to "More" and click "Multi Measure". Enable "Measure all x slices" and "One row per slice".\
 Then click ok')
print('4. A results window should open. Save it as "Results.csv"')

if ao.ask_user_to_confirm_ROI_signals_were_generated:
    ans = ''
    while ans != 'yes':
        ans = input('If you have performed all the above steps, please type "yes" and press Enter: ')

# remove the first column from the .csv because it represents the frame which isn't necessary
csv_path = os.path.join(ao.directory, 'Results.csv')
remove_first_csv_column(csv_path)

signals_arr = convert_csv_to_array(csv_path, n_horizontal, n_vertical)

if ao.generate_ROI_signals_grid_plot:
    fig = grid_plot(csv_path, n_horizontal, n_vertical)
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
dist_adj_sim = distance_adjusted_similarity(signals_arr, n_horizontal, n_vertical)
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
                                                       n_horizontal=n_horizontal, n_vertical=n_vertical,
                                                       n_frames=n_frames)

if ao.generate_ROI_cluster_associations_plot:
    fig = visualize_roi_cluster_associations(roi_clusters_dict, n_clusters, roi_dims, img_dims)
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

representative_signals = compute_representative_signal(clusters, signals_arr)

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
    cluster_signals_video(video_path, roi_clusters_dict, representative_signals, n_frames, img_dims, roi_dims,
                          pixel_dtype)

timing['video'] = time.time() - start_time
print(f"Step 7 (generating video) : {timing['video']:.1f} seconds\n")
########################################################################################################################
print("Elapsed time:", time.time() - initial_time, "seconds")
