import warnings

import tifffile as tf


def get_n_frames(image: tf.TiffFile):
    """
    Used to get the number of frames (images) of a multi-image tiff. This can be tricky because it's stored in different
    locations.
    :param image: the .tif / .TIF / .tiff image
    :return: the number of frames
    """
    n_frames = None
    try:
        n_frames = image.imagej_metadata['images']
    except KeyError:
        warnings.warn("imagej_metadata['images'] couldn't be accesses to find the number of frames")

    if n_frames is None:
        n_frames = len(image.pages)

    if n_frames == 1:
        raise ValueError("Only one frame has been found. There should be multiple frames")

    print(f'{n_frames} frames have been detected.')
    return n_frames
