from PIL import Image, ImageSequence
import numpy as np


def image_info(image_path: str):
    with Image.open(image_path) as im:
        print(f'=== {image_path.split("/")[-1]} ===')
        print(f'info: {im.info}')
        print(f'format: {im.format}')
        print(f'mode: {im.mode}')
        print(f'size: {im.size}')
        print(f'width: {im.width}')
        print(f'height: {im.height}')
        print(f'getbands: {im.getbands()}')
        print()


def image_as_array(image_path: str) -> np.array:
    with Image.open(image_path) as im:
        # we initialize a numpy array where each dimension represents the following:
        # 0 -> frames of the video
        # 1 -> vertical number of pixels (rows)
        # 2 -> horizontal number of pixels (columns)
        # each element is the calcium imaging value for that pixel TODO what does the element represent exactly?

        arr = np.zeros((im.n_frames, im.height, im.width))

        # now we go through each frame and fill the array
        for frame_index, frame in enumerate(ImageSequence.Iterator(im)):
            arr[frame_index, :, :] = np.array(frame)

    return arr
