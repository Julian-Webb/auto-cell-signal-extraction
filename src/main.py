import os
from generate_rois import generate_rois_from_size, save_rois

# base_path = '/Users/julian/development/PycharmProjects/glioblastoma/'
# calcium_img_path = 'data/01_raw/276_AZD3965_Mathieu.TIF'
# test_img_path = 'data/01_raw/test_stack/TestStack.tif'
# simple_test_stack = 'data/01_raw/simple_test_image/simple_test_stack.tif'
#
# image_array = image_as_array(base_path + test_img_path)

test_stack_dir = '/Users/julian/development/PycharmProjects/glioblastoma/data/01_raw/high_res_test_stack/'
image_path = os.path.join(test_stack_dir, 'high_res_test_stack.tif')

# Step 1 & 2: Load the image and compute the regions of interest (ROIs)
generated_rois = generate_rois_from_size(image_path, 512, 256)
save_rois(generated_rois, test_stack_dir)

# Step 3: Generate the signals based on the ROIs


# Step 4: Estimate which signals are duplicates

# Step 5: Filter out duplicate signals and save the result

