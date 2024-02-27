# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 14:12:37 2024
@author: estel

Simple script used to average all the slices in the original .tiff files and tweak pixel intensity
to improve image quality.
--> INPUT = raw .tiff stacks
--> OUTPUT1 = flattened image average as a .tiff in a sub-folder in the same directory as the input files
--> OUTPUT2 = .csv table containing file path, image ID, X, Y and Z value for each image
"""

# Import basic necessary packages/functions
import os
from os.path import dirname
import glob
import numpy as np

# Import the scikit-image package https://scikit-image.org/
# which allows loading stacks into numpy 3D arrays
import skimage as ski
#  Import tkinter for user input interface
from tkinter import Tk
from tkinter.filedialog import askdirectory  # User input interface

# Import relevant functions from other scripts
from Z_proj_functions import z_proj_average
from Z_proj_functions import stretch_intensity
from Z_proj_functions import theoretical_coordinates_table

# Get main path
outer_dir = dirname(os.getcwd())
# Ask user the path to the raw data (stack .tiff files)
root = Tk()
root.attributes("-topmost", True)
root.withdraw()
stack_path = askdirectory(initialdir=outer_dir, title='Select Folder containing .tiff stacks')
print(stack_path)

# Create an output directory if it doesn't exist
output_path = stack_path + "/Z_proj"
os.makedirs(output_path, exist_ok=True)  # exist_ok set to true to not raise an error if the folder exists
# Set fixed variables
slice_nbr = 200

# Find all stack .tiff in the selected directory
path = stack_path + '/*.tiff'
stack_files = glob.glob(path, recursive=False)
nbr_files = len(stack_files)

# Loop through the list of files, apply Z average projection and enhance contrast
for i in range(0, nbr_files):
    image_name = os.path.basename(stack_files[i])
    print(image_name)
    # Make sure files are numbered properly (i.e. no duplicate ID)
# THIS DOESN'T WORK IF THE IMAGES ARE NOT IN THE CORRECT ORDER
# I.E. ALTERNATING ZERO AND TRANSLATION (0,0,0) - (x,0,0) - (0,0,0) ...
    if i > 1:
        previous_image_name = os.path.basename(stack_files[i-1])
        image_id = int(image_name.split('_')[0])
        previous_id = int(previous_image_name.split('_')[0])
        if image_id == previous_id:
            new_id = str(image_id+1).zfill(3)
            image_name = new_id + image_name[image_name.index('_'):]
    # Open image and extract stack size
    im = ski.io.imread(stack_files[i], dtype=np.uint16)
    # check stack is 200 slices
    if im.shape[0] == slice_nbr:
        print('Correct slide number in file %s' % image_name)
        # Apply Z stack on slices (2 to im_size)
        im = z_proj_average(im)
        # Increase contrast
        im = stretch_intensity(im)
        # ski.io.imshow(im) (use to show image when testing only
        # Save as a new .tiff file
        ski.io.imsave(output_path + "/Flat_" + image_name, im)
    else:
        print('Not enough slices in file : %s' % image_name)

# Create a table containing all coordinates for each file
theoretical_coordinates_table(output_path)
