import time

import analysis_options as ao
from src.A_load_image_data.load_image_data import load_image_data
from src.C_get_ROI_signals.get_roi_signals import get_roi_signals
from src.D_remove_empty_rois.remove_empty_rois import remove_empty_rois
from src.D_remove_empty_rois.visualization.plot_roi_stds import plot_roi_stds
from src.F_cluster_ROIs.visualize_dendrogram import visualize_dendrogram
from src.G_representative_signals.save_repr_signals import save_repr_signals
from src.utils.ROI import ROI
from src.B_generate_rois.generate_rois_from_size import generate_rois_from_size
from src.B_generate_rois.save_imagej_rois import save_imagej_rois
from src.C_get_ROI_signals.visualization.single_plot import single_plot
from src.C_get_ROI_signals.visualization.grid_plot import grid_plot
from src.E_calculate_roi_distances.roi_distances import roi_distances
from src.F_cluster_ROIs.cluster_rois import cluster_rois
from src.F_cluster_ROIs.visualize_roi_cluster_associations import visualize_roi_cluster_associations
from src.G_representative_signals.compute_representative_signals import compute_representative_signals
from src.G_representative_signals.visualization.cluster_signals_video import cluster_signals_video
from src.G_representative_signals.visualization.plot_repr_signals import plot_repr_signals

initial_time = time.time()

# ##### Step A: Load the image data ####################################################################################
#
print('### A: Loading image data...')
n_frames, img_dims, pixel_dtype = load_image_data(ao.image_path)

#
#
# ##### Step B: Compute the regions of interest (ROIs) #################################################################
#
print('### B: Generating ROIs...', end='')
st = time.time()  # start time
rois = generate_rois_from_size(img_dims)
print(f'{(time.time() - st):.1f}s')

print('Saving ROIs...', end='')
save_imagej_rois(rois)  # this operation takes very long/crashes for very large number of ROIs (>3 Mio. ROIs)
print(f'{(time.time() - st):.1f}s')

print(f"\nA grid of {ROI.N_HORIZONTAL} x {ROI.N_VERTICAL} (horizontal x vertical) ROIs has been created. \
That makes {ROI.N_HORIZONTAL * ROI.N_VERTICAL} ROIs.\n")

#
#
# ##### Step C: Get the signals based on the ROIs ######################################################################
#
print('### C: Getting ROI signals...', end='')
st = time.time()
signals_arr, full_signals_df = get_roi_signals(ao.image_path, n_frames, rois)
print(f'{time.time() - st:.1f}s')

print('ROI signals to csv...', end='')
st = time.time()
full_signals_df.to_csv(ao.roi_signals_csv_path)
print(f'{time.time() - st:.1f}s')

if ao.generate_ROI_signals_grid_plot:
    print('Generating ROI signals grid plot...', end='')
    st = time.time()
    grid_plot(signals_arr).savefig(ao.roi_signals_grid_plot_path)
    print(f'{time.time() - st:.1f}s')

if ao.generate_ROI_signals_single_plot:
    st = time.time()
    print('Generating ROI signals single plot...', end='')
    single_plot(full_signals_df).savefig(ao.roi_signals_single_plot_path)
    print(f'{time.time() - st:.1f}s')

#
#
# ##### Step D: Remove empty ROIs ######################################################################################
#
# We want to remove ROIs that don't contain a cell
if ao.generate_ROI_stds_plot:
    print('### D: Plotting ROI standard deviations...', end='')
    st = time.time()
    plot_roi_stds(signals_arr, rois, img_dims, ao.std_threshold).savefig(ao.roi_stds_plot_path)
    print(f'{time.time() - st:.1f}s')


print('### D: Removing empty ROIs...', end='')
st = time.time()
signals_df, filtered_rois, removed_rois = remove_empty_rois(full_signals_df.copy(), ao.std_threshold)
print(f'{time.time() - st:.1f}s')

print(f'\n{removed_rois.size} empty ROIs have been detected and filtered out. \
Remaining ROIs: {ROI.N_HORIZONTAL * ROI.N_VERTICAL - removed_rois.size}\n')

print('Filtered ROI signals to csv...', end='')
st = time.time()
signals_df.to_csv(ao.filtered_roi_signals_csv_path)
print(f'{time.time() - st:.1f}s')
#
#
# ##### Step E: Compute the distance measure between the ROIs ##########################################################
#
# We calculate the distance for each pair of ROIs
print('### E: Computing ROI distance matrix...', end='')
st = time.time()
roi_distances = roi_distances(signals_df, filtered_rois)
print(f'{time.time() - st:.1f}s')

print('Saving ROI distance matrix to csv...', end='')
st = time.time()
roi_distances.to_csv(ao.roi_distances_csv_path)
print(f'{time.time() - st:.1f}s')

#
#
# ##### Step F: Create clusters based on similarity ####################################################################
#
print('### F: Creating clusters...', end='')
st = time.time()

clusters, n_clusters, roi_clusters_dict, clustering_steps = cluster_rois(roi_distances, filtered_rois)

print(f'{time.time() - st:.1f}s')

if ao.generate_ROI_cluster_associations_plot:
    print('Generating ROI-cluster associations plot...', end='')
    st = time.time()
    visualize_roi_cluster_associations(roi_clusters_dict, n_clusters, img_dims, removed_rois).savefig(
        ao.roi_cluster_associations_path)
    print(f'{time.time() - st:.1f}s')

if ao.generate_dendrogram:
    print('Generating Dendrogram...', end='')
    st = time.time()
    visualize_dendrogram(clustering_steps, filtered_rois).savefig(ao.dendrogram_path)
    print(f'{time.time() - st:.1f}s')

#
#
# ##### Step G: Create/Select a representative signal for each cluster/cell and save the result ########################
#
print("### G: Computing representative signals...", end='')
st = time.time()
repr_signals = compute_representative_signals(clusters, signals_df, n_clusters, n_frames)
save_repr_signals(repr_signals, n_clusters)
print(f'{time.time() - st:.1f}s')

if ao.generate_signals_per_cluster_plot:
    print('Generating signals per cluster plot...', end='')
    plot_repr_signals(repr_signals).savefig(ao.signal_per_cluster_plot_path)
    print(f'{time.time() - st:.1f}s')

# create video
if ao.generate_cluster_signals_video:
    print('Generating cluster signals video...', end='')
    st = time.time()
    cluster_signals_video(ao.cluster_signals_video_path, roi_clusters_dict, repr_signals, n_frames,
                          img_dims, pixel_dtype)
    print(f'{time.time() - st:.1f}s')

########################################################################################################################
print(f"Total elapsed time: {(time.time() - initial_time):.1f}s")
