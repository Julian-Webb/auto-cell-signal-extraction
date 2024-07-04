import time
import options as opt
from src.A_load_image_data.load_image_data import load_image_data
from src.B_generate_rois.visualization.rois_on_image import rois_on_image
from src.C_get_ROI_signals.get_roi_signals import get_roi_signals
from src.D_detrend_signals.detrend_signals import detrend_signals
from src.E_remove_empty_rois.remove_empty_rois import remove_empty_rois
from src.E_remove_empty_rois.visualization.roi_stds_on_image import plot_roi_stds_on_image
from src.G_cluster_ROIs.visualization.clusters_on_image import clusters_on_image
from src.G_cluster_ROIs.visualization.dendrogram import visualize_dendrogram
from src.H_representative_signals.save_repr_signals import save_repr_signals
from src.utils.ROI import ROI
from src.B_generate_rois.generate_rois_from_size import generate_rois_from_size
from src.B_generate_rois.save_imagej_rois import save_imagej_rois
from src.C_get_ROI_signals.visualization.single_plot import single_plot
from src.C_get_ROI_signals.visualization.grid_plot import grid_plot
from src.F_calculate_roi_distances.roi_distances import calculate_roi_distances
from src.G_cluster_ROIs.cluster_rois import agglomerative_clustering, k_means, k_means_spatial_weighted
from src.G_cluster_ROIs.visualization.roi_cluster_associations import visualize_roi_cluster_associations
from src.H_representative_signals.compute_representative_signals import compute_representative_signals
from src.H_representative_signals.visualization.cluster_signals_video import cluster_signals_video
from src.H_representative_signals.visualization.plot_cluster_signals import plot_cluster_signals


def main():
    # %%
    print('--- A: Load Image Data ---')
    n_frames_raw, img_dims, pixel_dtype = load_image_data(opt.image_path)

    # %%
    print('\n--- B: Compute ROIs ---')
    all_rois = generate_rois_from_size(img_dims)

    # printing ROI / image information
    print(f'\n{opt.image_name.split("/")[-1]} (image name)')
    print(f'ROI width, height: {ROI.WIDTH_PIXELS} x {ROI.HEIGHT_PIXELS} px')
    print(
        f"A grid of {ROI.N_HORIZONTAL} x {ROI.N_VERTICAL} (horizontal x vertical) ROIs has been created. \
        That makes {ROI.N_HORIZONTAL * ROI.N_VERTICAL} ROIs.\n")

    if opt.B_save_imagej_rois:
        # this operation takes very long/crashes for very large number of ROIs (>3 Mio. ROIs)
        save_imagej_rois(all_rois)

    if opt.B_plot_rois_on_image:
        rois_on_image(opt.image_path, img_dims).savefig(opt.B_plot_rois_on_image_path, bbox_inches='tight')

    # %%
    print('\n--- C: Get ROI signals ---')
    signals_arr, all_signals_df = get_roi_signals(opt.image_path, n_frames_raw, all_rois,
                                                  opt.roi_signal_summary_statistic)

    if opt.C_create_all_ROI_signals_file:
        print('All ROI signals to csv...', end='')
        st = time.time()
        all_signals_df.to_csv(opt.C_roi_signals_csv_path)
        print(f'{time.time() - st:.1f}s')

    if opt.C_generate_ROI_signals_grid_plot:
        grid_plot(all_signals_df).savefig(opt.C_roi_signals_grid_plot_path, bbox_inches='tight')

    if opt.C_generate_ROI_signals_single_plot:
        single_plot(all_signals_df).savefig(opt.C_roi_signals_single_plot_path)

    # %%
    print('\n--- D: Detrending ROI signals ---')
    detrended_signals_df, n_frames_detrended = detrend_signals(all_signals_df, opt.rolling_window_size)
    del all_signals_df

    if opt.D_create_detrended_signals_file:
        print('Saving detrended signals...')
        detrended_signals_df.to_csv(opt.D_detrended_signals_csv_path)

    if opt.D_generate_detrended_signals_grid_plot:
        grid_plot(detrended_signals_df, {'color': 'green'}).savefig(opt.D_detrended_signals_grid_plot_path,
                                                                    bbox_inches='tight')

    if opt.D_generate_detrended_signals_single_plot:
        single_plot(detrended_signals_df).savefig(opt.D_detrended_signals_single_plot_path)

    # %%
    # We want to remove ROIs that don't contain a cell
    print('\n--- E: Removing empty ROIs ---')
    filtered_signals_df, filtered_rois, removed_rois = remove_empty_rois(detrended_signals_df.copy(), opt.std_threshold)

    if opt.E_plot_ROI_stds_on_image:
        plot_roi_stds_on_image(detrended_signals_df, img_dims, opt.std_threshold, opt.image_path,
                               # filtered_rois=filtered_rois,
                               removed_rois=removed_rois,
                               ).savefig(opt.E_roi_stds_plot_path, bbox_inches='tight')

    print(f'\n{removed_rois.size} empty ROIs have been detected and filtered out. \
    Remaining ROIs: {ROI.N_HORIZONTAL * ROI.N_VERTICAL - removed_rois.size}\n')

    if opt.E_create_filtered_ROI_signals_file:
        print('Filtered ROI signals to csv...', end='')
        st = time.time()
        filtered_signals_df.to_csv(opt.E_filtered_roi_signals_csv_path)
        print(f'{time.time() - st:.1f}s')

    # %%
    if opt.clustering_method == 'agglomerative':
        # We calculate the distance for each pair of ROIs
        print('\n--- F: Computing ROI distance matrix ---')
        roi_distances = calculate_roi_distances(filtered_signals_df, opt.F_spatial_comparison_range_pixels)

        if opt.F_create_ROI_distances_file:
            print('Saving ROI distance matrix to csv...', end='')
            st = time.time()
            roi_distances.to_csv(opt.F_roi_distances_csv_path)
            print(f'{time.time() - st:.1f}s')

        print('\n--- G: Agglomerative Clustering ---')
        clusters, n_clusters, roi_cluster_dict, clustering_steps = \
            agglomerative_clustering(roi_distances, filtered_rois, opt.max_clusters)

        if opt.G_plot_dendrogram:
            visualize_dendrogram(clustering_steps, filtered_rois).savefig(opt.G_dendrogram_path, bbox_inches='tight')

    elif opt.clustering_method == 'basic_kmeans':
        print('\n--- G: K-Means clustering ---')
        clusters, n_clusters, roi_cluster_dict = k_means(filtered_signals_df, opt.k_clusters)
    elif opt.clustering_method == 'spatial_weighted_kmeans':
        print('\n--- G: K-Means clustering ---')
        # clusters, n_clusters, roi_cluster_dict = do_k_means_spatial(filtered_signals_df, opt.k_clusters)
        clusters, n_clusters, roi_cluster_dict = \
            k_means_spatial_weighted(filtered_signals_df, opt.k_clusters, n_frames_detrended, opt.spatial_weight)
    else:
        raise ValueError(f"clustering_method is {opt.clustering_method}")

    if opt.G_plot_clusters_on_image:
        clusters_on_image(roi_cluster_dict, [], n_clusters, opt.image_path,
                          img_dims).savefig(opt.G_clusters_on_image_path, bbox_inches='tight')

    if opt.G_plot_ROI_cluster_associations:
        visualize_roi_cluster_associations(roi_cluster_dict, n_clusters, img_dims, removed_rois).savefig(
            opt.G_roi_cluster_associations_path, bbox_inches='tight')

    # %%
    print("\n--- H: Computing representative signals for each cluster ---")
    repr_signals, repr_rois = compute_representative_signals(clusters, filtered_signals_df, n_clusters,
                                                             n_frames_detrended)
    save_repr_signals(repr_signals, repr_rois, n_clusters)

    if opt.H_plot_clusters_and_representative_rois_on_image:
        clusters_on_image(roi_cluster_dict, repr_rois, n_clusters, opt.image_path,
                          img_dims).savefig(opt.H_clusters_on_image_path, bbox_inches='tight')

    if opt.H_plot_signals_per_cluster:
        plot_cluster_signals(repr_signals).savefig(opt.H_signal_per_cluster_plot_path)

    # create video
    if opt.H_generate_cluster_signals_video:
        cluster_signals_video(opt.H_cluster_signals_video_path, roi_cluster_dict, repr_signals, n_frames_detrended,
                              img_dims, pixel_dtype)


if __name__ == '__main__':
    initial_time = time.perf_counter()
    main()
    print(f"Total elapsed time: {(time.perf_counter() - initial_time):.1f}s")
