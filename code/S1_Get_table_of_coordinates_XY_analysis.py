"""
Created on 28 May 2024
@author: Estelle

This script loops through the chosen data folders and creates a csv file containing image path, ID, X, Y and Z.
It uses a function from "Function_1_Find_nearest_images_XY_analysis.py" to detect the nearest files at location (0;0;0) relative
to the image of interest.

--> INPUT = All the raw .tiff images
--> OUTPUT = Table of coordinates containing all the relevant variables

"""
# Import basic necessary packages/functions
import os
from os.path import dirname
import glob
import numpy as np
import pandas as pd
import re
from datetime import datetime

#  Import tkinter for user input interface
from tkinter import Tk
from tkinter.filedialog import askdirectory  # User input interface

# Import relevant functions from other scripts
from Function_1_Find_nearest_images_XY_analysis import find_nearest_zero

# Import the scikit-image package https://scikit-image.org/
# which allows loading stacks into numpy 3D arrays
import skimage as ski

# Get main path
outer_dir = dirname(os.getcwd())
# Ask user the path to the raw data (stack .tiff files)
root = Tk()
root.attributes("-topmost", True)
root.withdraw()
stack_path = askdirectory(initialdir=outer_dir, title='Select Folder containing .tiff stacks')
print(stack_path)

# Create an output directory to save the list of variable (if it doesn't exist)
output_path = outer_dir + "/Data"
os.makedirs(output_path, exist_ok=True)  # exist_ok set to true to not raise an error if the folder exists

# Set fixed variables
slice_nbr = 200

# Find all stack .tiff in the selected directory
path = stack_path + '/**/*.tiff'
stack_files = glob.glob(path, recursive=True)
nbr_files = len(stack_files)

# Create lists to store image ID and theoretical coordinates
path_list = []
image_name_list = []
protocol_list = []
id_list = []
x_list = []
y_list = []
z_list = []
slice_nbr_list = []

for i in range(0, nbr_files):
    # Open image and extract stack size
    im = ski.io.imread(stack_files[i], dtype=np.uint16)
    # check stack is 200 slices
    if im.shape[0] == slice_nbr:
        print('Correct slide number in file')
        slice_nbr = im.shape[0]

        # get path and ID
        image_full_path = stack_files[i]
        image_name = os.path.splitext(os.path.basename(stack_files[i]))[0]
        print(image_name)
        image_id = image_name.split('_')[0].zfill(3)
        protocol = '_'.join(image_full_path.split('\\')[1].split(' ')[0:2])

        # get x , y and z values
        coordinate_string = image_name.replace(image_id + "_", "").replace("_", "")
        x = int(re.split(r'[xyz]', coordinate_string)[1])
        y = int(re.split(r'[xyz]', coordinate_string)[2])
        z = int(re.split(r'[xyz]', coordinate_string)[3])
        print("ID = ", image_id, ", X = ", x, ", Y = ", y, ", Z = ", z)

        # Append all variable to lists
        path_list.append(image_full_path)
        image_name_list.append(image_name)
        protocol_list.append(protocol)
        id_list.append(image_id)
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
        slice_nbr_list.append(slice_nbr)
    else:
        print('Not enough slices in file : %s' % stack_files[i])

# Create a file containing all the variables  by merging lists into a dataframe
coord_table = pd.DataFrame()
coord_table['Image_path'] = path_list
coord_table['Image_name'] = image_name_list
coord_table['Protocol'] = protocol_list
coord_table['ID'] = id_list
coord_table['Slice_number'] = slice_nbr_list
coord_table['X_input_steps'] = x_list
coord_table['Y_input_steps'] = y_list
coord_table['Z_input_steps'] = z_list
coord_table['X_input_microm'] = coord_table['X_input_steps'] / 2
coord_table['Y_input_microm'] = coord_table['Y_input_steps'] / 2
coord_table['Z_input_microm'] = coord_table['Z_input_steps'] / 2

# Create 2 temporary columns with absolute value of x and y to allow for a correct ordering of the file
coord_table = (coord_table.assign(X=coord_table['X_input_steps'].abs(),
                                  Y=coord_table['Y_input_steps'].abs())
               .sort_values(['Protocol', 'ID', 'X', 'Y'],  # Sort by Protocol, ID, and X and Y absolute values
                            ascending=[True, True, True, True])
               .drop(columns=['X', 'Y'], axis=1))  # Drops absolute columns

# save table as .csv
# current_time = datetime.now().strftime("%Y_%m_%d-%p%I_%M_%S")
# coord_table.to_csv(path_or_buf=output_path + '/Theoretical_coordinates_table_' + current_time + '.csv',
#                    sep=',',
#                    na_rep='NA',
#                    header=True,
#                    index=False,
#                    encoding='utf-8-sig')
# print(f'Coordinates table saved as csv : {output_path}/Theoretical_coordinates_table.csv')

# Exclude z stacks
table_no_z = coord_table[coord_table['Z_input_steps'] == 0].reset_index(drop=True)
# Add a numerical id based on the ordering of the files (Previously sorted by Protocol, ID, and X and Y absolute values)
table_no_z['Numeric_id'] = range(1, len(table_no_z) + 1)

# Create dictionary of dataframe for each protocol
protocol_name_list = table_no_z['Protocol'].unique()
dict_of_protocols = dict(tuple(table_no_z.groupby('Protocol')))

# Loop through all the protocols
# Apply a custom function to find the nearest (0,0,0) location images before and after
for j in range(0, len(protocol_name_list)):
    protocol_name = protocol_name_list[j]
    protocol = dict_of_protocols[protocol_name].reset_index(drop=True)
    protocol_updated = find_nearest_zero(protocol)
    dict_of_protocols[protocol_name] = protocol_updated
    # Save one table per protocol
    current_time = datetime.now().strftime("%Y_%m_%d-%p%I_%M_%S")
    protocol_updated.to_csv(
        path_or_buf=output_path + '/Table_of coordinate_' + protocol_name + '_' + current_time + '.csv',
        sep=',',
        na_rep='NA',
        header=True,
        index=False,
        encoding='utf-8-sig')
    print(f'Coordinates table of {protocol_name} saved as csv')

# Save a grouped table with all protocols
protocol_merged = pd.concat(dict_of_protocols.values(), ignore_index=True).reset_index(drop=True)
current_time = datetime.now().strftime("%Y_%m_%d-%p%I_%M_%S")
protocol_merged.to_csv(path_or_buf=output_path + '/Table_of coordinate_all_protocols_' + current_time + '.csv',
                       sep=',',
                       na_rep='NA',
                       header=True,
                       index=False,
                       encoding='utf-8-sig')
print(f'Coordinates table merged saved as csv')
