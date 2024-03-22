import tifffile as tf
from src.A_load_image_data.get_n_frames import get_n_frames
from src.utils.coordinate_system import Dimensions


def load_image_data(image_path):
    with tf.TiffFile(image_path) as image:
        n_frames = get_n_frames(image)

        # determine height and width
        img_dims = Dimensions(width=image.pages[0].shape[1], height=image.pages[0].shape[0])

        # determine datatype of pixel values (It needs to be the same for all frames!)
        pixel_dtype = image.asarray(key=0).dtype  # get the dtype for the first frame

    return n_frames, img_dims, pixel_dtype
