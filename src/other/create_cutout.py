# Creates a cutout of a .tif and saves it

from os.path import join
import os

from tifffile import TiffFile, imwrite

if __name__ == '__main__':
    base_dir = "/Users/julian/development/PycharmProjects/glioblastoma"
    file_path = join(base_dir, "data/233_NoMG_A1/raw/233_NoMG_A1_STACK.tif")
    save_dir = join(base_dir, "data/233_NoMG_A1_cutout/raw/")
    save_path = join(save_dir, '233_NoMG_A1_STACK_cutout.tif')

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # these are inclusive indexes
    x_start, x_stop = 240, 1200
    y_start, y_stop = 0, 608

    with TiffFile(file_path) as tif:

        # has shape: (n_frames, height, width)
        image = tif.asarray()

        cutout = image[:, y_start:y_stop, x_start:x_stop]

    # save the cutout
    imwrite(save_path, cutout)
