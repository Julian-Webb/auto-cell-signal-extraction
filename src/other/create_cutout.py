# Creates a cutout of a .tif and saves it

from os.path import join
import os

from tifffile import TiffFile, imwrite

if __name__ == '__main__':
    base_dir = "/"
    file_path = join(base_dir, "data/233_NoMG_A1_cutout/raw/233_NoMG_A1_STACK_cutout.tif")
    save_dir = join(base_dir, "data/single_cell/raw/")
    save_path = join(save_dir, 'single_cell.tif')

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # these are inclusive indexes
    x_start = 0
    x_stop = x_start + 32
    y_start = 96
    y_stop = y_start + 160

    with TiffFile(file_path) as tif:

        # has shape: (n_frames, height, width)
        image = tif.asarray()

        cutout = image[:, y_start:y_stop, x_start:x_stop]

    # save the cutout
    imwrite(save_path, cutout)
