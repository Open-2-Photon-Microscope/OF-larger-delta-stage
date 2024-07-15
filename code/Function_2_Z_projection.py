""""
Created on 30 May 2024
@author: Estelle

Set of functions used with "S2_Z_projection_and_contrast_enhancement.py"
"""

# Import basic necessary packages/functions
import numpy as np

# Import the scikit-image package https://scikit-image.org/
# which allows loading stacks into numpy 3D arrays
import skimage as ski


# Function creating a Z projection across slices (2 to im_size)
# Input image as numpy array, returns new array
def z_proj_average(image):
    image = image[1:, :, :]  # Removes first slice as it often present recording issues such as empty pixel lines
    im_height = image.shape[1]
    im_width = image.shape[2]
    values = []
    for i in range(im_height):
        for j in range(im_width):
            values.append((np.mean(image[:, i, j])))

    values = np.array([values])
    values = values.reshape(im_height, im_width)
    return values


# Function enhancing contrast by stretching intensity values across the entire range + normalising intensity
# Input image name, output high contrast image
def stretch_intensity(image):
    # Stretch the range of pixel intensity across the 16bits range from 2nd to 98th percentile
    minval = np.percentile(image, 2)
    maxval = np.percentile(image, 98)
    image = np.clip(image, minval, maxval)
    image = ((image - minval) / (maxval - minval)) * 65535
    # Check min and max after transformation
    # print('Min: %.3f, Max: %.3f' % (image.min(), image.max()))
    # Normalise pixel values between 0 and 1 on a 16bits image
    image /= 65535
    # Convert back to a 16bits image
    image = ski.util.img_as_uint(image)
    return image
