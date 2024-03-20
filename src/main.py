import os
import time
import tifffile as tf
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

start_time = time.time()

# ##### Step 0.0: Path Initialization ##################################################################################
# Please specify your desired paths

base_dir = '/Users/julian/development/PycharmProjects/glioblastoma'

# calcium image
# calcium_img_dir = os.path.join(base_dir, 'data', '01_raw', '276_AZD3965_Mathieu')
# calcium_img_path = os.path.join(calcium_img_dir, '276_AZD3965_Mathieu.TIF')
# directory = calcium_img_dir
# image_path = calcium_img_path

# test stack
test_stack_dir = os.path.join(base_dir, 'data', '01_raw', 'high_res_test_stack')
test_stack_path = os.path.join(test_stack_dir, 'high_res_test_stack.tif')
directory = test_stack_dir
image_path = test_stack_path

# single image
# single_image_dir = '/Users/julian/development/PycharmProjects/glioblastoma/data/01_raw/single_image/'
# single_image_path = os.path.join(single_image_dir, 'single_image.tiff')


# make figures directory
figures_dir = os.path.join(directory, 'figures')
if not os.path.exists(figures_dir):
    os.mkdir(figures_dir)

# ##### Step 1: Load the image #########################################################################################
with tf.TiffFile(image_path) as image:
    n_frames = get_n_frames(image)

    # determine height and width
    img_dims = Dimensions(width=image.pages[0].shape[1], height=image.pages[0].shape[0])

    # determine datatype of pixel values (It needs to be the same for all frames!)
    pixel_dtype = image.asarray(key=0).dtype  # get the dtype for the first frame

# ##### Step 0.1: Specify ROI size ##################################################################################
roi_dims = Dimensions(img_dims.width // 4, img_dims.height // 4)

# ##### Step 2: Compute the regions of interest (ROIs) #################################################################
rois_dict = generate_rois_from_size(img_dims, roi_dims)
save_rois(rois_dict["rois"], directory)
n_horizontal, n_vertical = rois_dict["n_horizontal"], rois_dict["n_vertical"]
print(f"\nA {n_horizontal} x {n_vertical} grid of ROIs has been created.\n")

# ##### Step 3: Generate the signals based on the ROIs #################################################################
# The user needs to do this manually with Fiji
print('Please manually perform the following steps now:')
print('1. Drag the image and the ROIs into Fiji.')
print('2. Open the ROI Manager, go to "More" and click "Sort". The ROIs should get sorted')
print('3. Then go to "More" and click "Multi Measure". Enable "Measure all x slices" and "One row per slice".\
 Then click ok')
print('4. A results window should open. Save it as "Results.csv"')

ans = ''
while ans != 'yes':
    ans = input('If you have performed all the above steps, please type "yes" and press Enter: ')

# remove the first column from the .csv because it represents the frame which isn't necessary
csv_path = os.path.join(directory, 'Results.csv')
remove_first_csv_column(csv_path)
signals_arr = convert_csv_to_array(csv_path, n_horizontal, n_vertical)

fig = grid_plot(csv_path, n_horizontal, n_vertical)
fig.savefig(os.path.join(figures_dir, 'grid_plot.png'))
del fig

fig = single_plot(csv_path)
fig.savefig(os.path.join(figures_dir, 'single_plot.png'))
del fig

# ##### Step 4: Estimate which signals are duplicates ##################################################################
# We calculate the distance-adjust signal similarity for each pair of ROIs
dist_adj_sim = distance_adjusted_similarity(signals_arr, n_horizontal, n_vertical)
dist_adj_sim.to_csv(os.path.join(directory, 'Distance-adjusted similarity.csv'))

# ##### Step 5: Create clusters based on similarity ####################################################################
clusters, n_clusters, roi_clusters_dict = cluster_rois(dist_adj_sim, signals_arr, similarity_threshold=0.7,
                                                       n_horizontal=n_horizontal)

fig = visualize_roi_cluster_associations(roi_clusters_dict, n_clusters, roi_dims, img_dims)
fig.savefig(os.path.join(figures_dir, 'ROI-cluster_associations.png'))
del fig

# ##### Step 6: Create/Select a representative signal for each cluster/cell and save the result ########################
representative_signals = compute_representative_signal(clusters, signals_arr)

fig = plot_representative_signals(representative_signals)
fig.savefig(os.path.join(figures_dir, 'signal_per_cluster.png'))
del fig

# create video
video_path = os.path.join(figures_dir, 'cluster_signals_video.tif')
cluster_signals_video(video_path, roi_clusters_dict, representative_signals, n_frames, img_dims, roi_dims, pixel_dtype)
del video_path

########################################################################################################################
print("Elapsed time:", time.time() - start_time, "seconds")
