import skimage
import imagej
import os

# the example can be found here: https://py.imagej.net/en/latest/11-Working-with-the-original-ImageJ.html

# the macro
background_clear_and_crop = """
setBatchMode(true);

// Compute image background.
original = getImageID();
run("Duplicate...", " ");
run("Median...", "radius=6");
setAutoThreshold("Li dark");
run("Create Selection");

// Clear background of the original image.
selectImage(original);
run("Restore Selection");
setBackgroundColor(0, 0, 0);
run("Clear Outside");

// Crop to center portion of the image.
x = getWidth() / 4
y = getHeight() / 4
makeRectangle(x, y, x*2, y*2);
run("Crop");
rename(getTitle() + "-cropped")
"""

ij = imagej.init()

# load image
coins = skimage.data.coins()
ij.py.show(coins)

# convert to imagePlus
coins_plus = ij.py.to_imageplus(coins)
coins_plus.setTitle("coins")
coins_plus.show()

# make sure there is an active window/image
assert ij.WindowManager.getImage("coins") is not None

# run macro
ij.py.run_macro(background_clear_and_crop)

# see which windows are open
for imp_id in ij.WindowManager.getIDList():
    print(ij.WindowManager.getImage(imp_id))


# access the "coins-cropped" window
coins_cropped = ij.WindowManager.getImage("coins-cropped")
print(f"coins_cropped dims: {coins_cropped.dims}\ncoins_cropped shape: {coins_cropped.shape}")

# see the cropped image
ij.py.show(coins_cropped)

# there is a bug with the viewer when changing the dimensions, so we duplciate the image first
ij.py.show(coins_cropped.duplicate())