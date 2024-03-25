import time

import analysis_options as ao
from src.A_load_image_data.load_image_data import load_image_data
from src.C_get_ROI_signals.get_roi_signals import get_roi_signals
from src.utils.ROI import ROI
from src.B_generate_rois.generate_rois_from_size import generate_rois_from_size
from src.B_generate_rois.save_imagej_rois import save_imagej_rois
from src.C_get_ROI_signals.visualization.single_plot import single_plot
from src.C_get_ROI_signals.visualization.grid_plot import grid_plot
from src.D_calculate_similarity.distance_adjusted_similarity import distance_adjusted_similarity
from src.E_cluster_ROIs.cluster_rois import cluster_rois
from src.E_cluster_ROIs.visualize_roi_cluster_associations import visualize_roi_cluster_associations
from src.F_representative_signals.compute_representative_signals import compute_representative_signals
from src.F_representative_signals.visualization.cluster_signals_video import cluster_signals_video
from src.F_representative_signals.visualization.plot_repr_signals import plot_repr_signals

timing = {}
initial_time = time.time()

# ##### Step A: Load the image data ####################################################################################
start_time = time.time()

n_frames, img_dims, pixel_dtype = load_image_data(ao.image_path)

timing['Step A'] = time.time() - start_time
#
#
# ##### Step B: Compute the regions of interest (ROIs) #################################################################
#
start_time = time.time()

rois = generate_rois_from_size(img_dims)
save_imagej_rois(rois)

print(f"\nA grid of {ROI.N_HORIZONTAL} x {ROI.N_VERTICAL} (horizontal x vertical) ROIs has been created.\n")

timing['Step B'] = time.time() - start_time
print(f"Step B (computing ROIs) : {timing['Step B']:.1f} seconds\n")
#
#
# ##### Step C: Get the signals based on the ROIs ######################################################################
#
start_time = time.time()

signals_arr, signals_df = get_roi_signals(ao.image_path, n_frames, rois)
signals_df.to_csv(ao.roi_signals_csv_path)

if ao.generate_ROI_signals_grid_plot:
    grid_plot(signals_arr).savefig(ao.roi_signals_grid_plot_path)

if ao.generate_ROI_signals_single_plot:
    single_plot(signals_df).savefig(ao.roi_signals_single_plot_path)

timing['Step C'] = time.time() - start_time
print(f"Step C (computing ROI signals with FIJI) : {timing['Step C']:.1f} seconds\n")
#
#
# ##### Step D: Compute the similarity of the ROIs #####################################################################
#
start_time = time.time()
print('Computing distance-adjusted similarity matrix...', end='')

# We calculate the distance-adjust signal similarity for each pair of ROIs
dist_adj_sim = distance_adjusted_similarity(signals_arr, ROI.N_HORIZONTAL, ROI.N_VERTICAL)
dist_adj_sim.to_csv(ao.distance_adjusted_similarity_path)

print('Done')
timing['Step D'] = time.time() - start_time
print(f"Step D (computing similarity) : {timing['Step D']:.1f} seconds\n")
#
#
# ##### Step E: Create clusters based on similarity ####################################################################
#
start_time = time.time()
print('Creating clusters...', end='')

clusters, n_clusters, roi_clusters_dict = cluster_rois(dist_adj_sim, signals_arr, similarity_threshold=0.7,
                                                       n_horizontal=ROI.N_HORIZONTAL, n_vertical=ROI.N_VERTICAL,
                                                       n_frames=n_frames)

if ao.generate_ROI_cluster_associations_plot:
    visualize_roi_cluster_associations(roi_clusters_dict, n_clusters, img_dims).savefig(
        ao.roi_cluster_associations_path)

print('Done')
timing['Step E'] = time.time() - start_time
print(f"Step E (clustering) : {timing['Step E']:.1f} seconds\n")
#
#
# ##### Step F: Create/Select a representative signal for each cluster/cell and save the result ########################
#
start_time = time.time()

repr_signals = compute_representative_signals(clusters, signals_arr)

timing['Step F'] = time.time() - start_time
print(f"Step F (computing representative signals) : {timing['Step F']:.1f} seconds\n")

if ao.generate_signals_per_cluster_plot:
    plot_repr_signals(repr_signals).savefig(ao.signal_per_cluster_plot_path)

# create video
start_time = time.time()

if ao.generate_cluster_signals_video:
    cluster_signals_video(ao.cluster_signals_video_path, roi_clusters_dict, repr_signals, n_frames,
                          img_dims, pixel_dtype)

timing['video'] = time.time() - start_time
print(f"Generating video: {timing['video']:.1f} seconds\n")
########################################################################################################################
print(f"Elapsed time: {(time.time() - initial_time):.1f} seconds")
