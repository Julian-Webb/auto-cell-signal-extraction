import os
from generate_rois import generate_rois_from_size, save_rois
from generate_signals import remove_first_csv_column, convert_csv_to_array
from src.visualization.plot_signals_from_csv import ordered_subplots
import matplotlib as plt

# paths
base_dir = '/Users/julian/development/PycharmProjects/glioblastoma'

# calcium_img_path = 'data/01_raw/276_AZD3965_Mathieu.TIF'
# test_img_path = 'data/01_raw/test_stack/TestStack.tif'
# simple_test_stack = 'data/01_raw/simple_test_image/simple_test_stack.tif'

# test stack
test_stack_dir = os.path.join(base_dir, 'data', '01_raw', 'high_res_test_stack')
test_stack_path = os.path.join(test_stack_dir, 'high_res_test_stack.tif')

# single image
single_image_dir = '/Users/julian/development/PycharmProjects/glioblastoma/data/01_raw/single_image/'
single_image_path = os.path.join(single_image_dir, 'single_image.tiff')

directory = test_stack_dir
image_path = test_stack_path

# Step 1 & 2: Load the image and compute the regions of interest (ROIs)
rois_dict = generate_rois_from_size(image_path, 2048//16, 1536//16)
save_rois(rois_dict["rois"], directory)
print(f"\nA {rois_dict['n_horizontal']}x{rois_dict['n_vertical']} grid of ROIs has been created.\n")

# Step 3: Generate the signals based on the ROIs
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
arr = convert_csv_to_array(csv_path, rois_dict["n_horizontal"], rois_dict["n_vertical"])

fig = ordered_subplots(csv_path, rois_dict["n_horizontal"], rois_dict["n_vertical"])
fig.savefig('my_plot.png')

# Step 4: Estimate which signals are duplicates

# Step 5: Filter out duplicate signals and save the result
