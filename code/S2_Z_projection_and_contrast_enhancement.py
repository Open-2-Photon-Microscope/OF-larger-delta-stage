# -*- coding: utf-8 -*-
"""
Created on 30 May 2024
@author: Estelle

Script used to average all the slices in the original .tiff files and tweak pixel intensity
to improve image quality.

It uses 2 functions defined in "Function_2_Z_projection.py"

--> INPUT = Table of coordinates containing the path to the raw .tiff stacks of interest
--> OUTPUT1 = Flattened image Z projected average as a .tiff
--> OUTPUT2 = New table of coordinate updated to contain the files paths of the Z projected images instead of the raw data
"""

# Import basic necessary packages/functions
import os
from os.path import dirname
import numpy as np
import pandas as pd
from datetime import datetime
# Import the scikit-image package https://scikit-image.org/
# which allows loading stacks into numpy 3D arrays
import skimage as ski
#  Import tkinter for user input interface
from tkinter import Tk
from tkinter.filedialog import askopenfilename  # User input interface

# Import relevant functions from other scripts
from Function_2_Z_projection import z_proj_average
from Function_2_Z_projection import stretch_intensity

# Get main path
outer_dir = dirname(os.getcwd())
outer_dir = input('enter path to files:') ##REMOVE 
# Ask user the path to the coordinate table (can be for a single protocol or all protocol merged)
root = Tk()
root.attributes("-topmost", True)
root.withdraw()
table_path = askopenfilename(initialdir=outer_dir, title='Select the table of coordinate containing files paths')
print(table_path)

# Read coordinate table
coord_table = pd.read_csv(table_path)

# Create an output directory if it doesn't exist to store the Z projected images
output_path = os.path.dirname(table_path) + "/Z_proj"
os.makedirs(output_path, exist_ok=True)  # exist_ok set to true to not raise an error if the folder exists
# Create an output directories if it doesn't exist for each protocol
protocol_name_list = coord_table['Protocol'].unique()
for k in range(0, len(protocol_name_list)):
    protocol_path = output_path + "/" + protocol_name_list[k]
    os.makedirs(protocol_path, exist_ok=True)  # exist_ok set to true to not raise an error if the folder exists

# Loop through the coordinates table, apply Z average projection and enhance contrast to each image
# Save image in the newly created folders (for each protocol)
# Save a new coordinate table containing the path to the Z_projected files

for i in range(0, len(coord_table)):
    image_path = coord_table['Image_path'][i]
    image_name = os.path.basename(image_path)
    protocol = coord_table['Protocol'][i]
    print(image_name)
    # Open image and extract stack size
    im = ski.io.imread(image_path, dtype=np.uint16)

    # Apply Z stack on slices (2 to im_size)
    im = z_proj_average(im)
    # Increase contrast
    im = stretch_intensity(im)
    # ski.io.imshow(im) (use to show image when testing)
    # Save as a new .tiff file
    new_path = output_path + '/' + protocol + '/Flat_' + image_name
    ski.io.imsave(new_path, im)

    # In the coordinate table, replace the raw image path with the Z projected image path
    coord_table = coord_table.replace({image_path: new_path}, regex=False)

# Save the new coordinate table
current_time = datetime.now().strftime("%Y_%m_%d-%p%I_%M_%S")
coord_table.to_csv(path_or_buf=output_path + '/Z_project_table_of coordinate_' + current_time + '.csv',
                   sep=',',
                   na_rep='NA',
                   header=True,
                   index=False,
                   encoding='utf-8-sig')
print(f'Z project coordinates table merged saved as csv')
