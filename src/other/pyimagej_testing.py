# Testing ImageJ
# Create an ImageJ2 gateway with the newest available version of ImageJ2.
import imagej
ij = imagej.init('/Applications/Fiji.app')

# Load an image.
# image_url = 'https://imagej.net/images/clown.jpg'
image_path = '/Users/julian/development/PycharmProjects/glioblastoma/data/01_raw/single_image/single_image.tiff'
jimage = ij.io().open(image_path)

# Convert the image from ImageJ2 to xarray, a package that adds
# labeled datasets to numpy (http://xarray.pydata.org/en/stable/).
image = ij.py.from_java(jimage)

# Display the image (backed by matplotlib).
ij.py.show(image, cmap='gray')

