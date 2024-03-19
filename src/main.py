import os
from PIL import Image
from generate_rois import generate_rois_from_size, save_rois
from generate_signals import remove_first_csv_column, convert_csv_to_array
from src.distance_adjusted_similarity import distance_adjusted_similarity
from src.cluster_rois import cluster_rois
from src.merge_clustered_signals import compute_representative_signal
from src.visualization.plot_representative_signals import plot_representative_signals
from src.visualization.plot_signals_from_csv import grid_plot, single_plot
from src.visualization.visualize_roi_cluster_associations import visualize_roi_cluster_associations

# ##### Step 0: Path Initialization ####################################################################################
# Please specify your desired paths

base_dir = '/Users/julian/development/PycharmProjects/glioblastoma'

# calcium image
# calcium_img_dir = os.path.join(base_dir, 'data', '01_raw', '276_AZD3965_Mathieu')
# calcium_img_path = os.path.join(calcium_img_dir, '276_AZD3965_Mathieu.TIF')

# test stack
test_stack_dir = os.path.join(base_dir, 'data', '01_raw', 'high_res_test_stack')
test_stack_path = os.path.join(test_stack_dir, 'high_res_test_stack.tif')

# single image
# single_image_dir = '/Users/julian/development/PycharmProjects/glioblastoma/data/01_raw/single_image/'
# single_image_path = os.path.join(single_image_dir, 'single_image.tiff')

directory = test_stack_dir
image_path = test_stack_path

# make figures directory
figures_dir = os.path.join(directory, 'figures')
if not os.path.exists(figures_dir):
    os.mkdir(figures_dir)

# ##### Step 1: Load the image #########################################################################################
with Image.open(image_path) as image:
    img_dims = (image.width, image.height)  # image dimensions

# ##### Step 2: Compute the regions of interest (ROIs) #################################################################
rois_dict = generate_rois_from_size(img_dims[0], img_dims[1], img_dims[0] // 4, img_dims[1] // 4)
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

fig = single_plot(csv_path)
fig.savefig(os.path.join(figures_dir, 'single_plot.png'))

# ##### Step 4: Estimate which signals are duplicates ##################################################################
# We calculate the distance-adjust signal similarity for each pair of ROIs
dist_adj_sim = distance_adjusted_similarity(signals_arr, n_horizontal, n_vertical)
dist_adj_sim.to_csv(os.path.join(directory, 'Distance-adjusted similarity.csv'))

# ##### Step 5: Create clusters based on similarity ####################################################################
clusters, n_clusters, roi_clusters_dict = cluster_rois(dist_adj_sim, signals_arr, similarity_threshold=0.7, n_horizontal=n_horizontal)

img_dims = (16, 12)
roi_dims = (img_dims[0] // n_horizontal, img_dims[1] // n_vertical)
fig = visualize_roi_cluster_associations(roi_clusters_dict, n_clusters, roi_dims, img_dims)
fig.savefig(os.path.join(figures_dir, 'ROI-cluster_associations.png'))


# ##### Step 6: Create/Select a representative signal for each cluster/cell and save the result ########################
representative_signals = compute_representative_signal(clusters, signals_arr)

fig = plot_representative_signals(representative_signals)
fig.savefig(os.path.join(figures_dir, 'signal_per_cluster.png'))

