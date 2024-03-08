import sys
import os

sys.path.append(os.getcwd() + '/1_data_input')
from input_tif import image_as_array

# TODO optimize folder structure and imports


base_path = '/Users/julian/development/PycharmProjects/glioblastoma/'
calcium_img_path = 'data/01_raw/276_AZD3965_Mathieu.TIF'
test_img_path = 'data/01_raw/test_stack/TestStack.tif'
simple_test_stack = 'data/01_raw/simple_test_image/simple_test_stack.tif'

image_array = image_as_array(base_path + test_img_path)

