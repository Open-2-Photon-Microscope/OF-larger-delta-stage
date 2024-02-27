# Set of functions used with "Z_projection_and_contrast_enhancement.py"

# Import basic necessary packages/functions
import os
import glob
import numpy as np
import pandas as pd

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


# Function extracting all theoretical coordinates information from filename
# Input the path of Z projected files, saves  a csv table containing file path, image ID, X, Y and Z value
def theoretical_coordinates_table(z_proj_path):
    # Find all .tiff in the selected directory
    path = z_proj_path + '/*.tiff'
    img_list = glob.glob(path, recursive=False)
    # Create lists to store image ID and theoretical coordinates
    id_list = []
    name_list = []
    x_list = []
    y_list = []
    z_list = []
    for i in range(0, len(img_list)):
        file_path = img_list[i]
        # Get relevant information in file name (i.e X,Y,Z and image ID)
        image_name = os.path.splitext(os.path.basename(file_path))[0]
        image_id = int(image_name.split('_')[1])
        x = int(image_name.split('_')[2].replace("x", ""))
        y = int(image_name.split('_')[3].replace("y", ""))
        z = int(image_name.split('_')[4].replace("z", ""))

        id_list.append(image_id)
        name_list.append(image_name)
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)

    # Merge lists into a dataframe
    coord_table = pd.DataFrame()
    coord_table['Image_path'] = img_list
    coord_table['Image_name'] = name_list
    coord_table['ID'] = id_list
    coord_table['X_input_steps'] = x_list
    coord_table['Y_input_steps'] = y_list
    coord_table['Z_input_steps'] = z_list
    coord_table['X_input_microm'] = coord_table['X_input_steps'] / 2
    coord_table['Y_input_microm'] = coord_table['Y_input_steps'] / 2
    coord_table['Z_input_microm'] = coord_table['Z_input_steps'] / 2

    print(f'Coordinates table saved as csv : {z_proj_path}/Theoretical_coordinates_table.csv')
    coord_table.to_csv(path_or_buf=z_proj_path + '/Theoretical_coordinates_table.csv',
                       sep=',',
                       na_rep='NA',
                       header=True,
                       index=False,
                       encoding='utf-8-sig')
