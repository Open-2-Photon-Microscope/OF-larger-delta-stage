"""
Created on 28 May 2024
@author: Estelle

This script loops through the chosen data folders and creates a csv file containing image path, ID, X, Y and Z.

It selects the correct images for t0, t1, t2, and t3

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

# Import the scikit-image package https://scikit-image.org/
# which allows loading stacks into numpy 3D arrays
import skimage as ski

# Get main path
outer_dir = input('Target folder (path): ')
if outer_dir == '':
    outer_dir = '/home/marcus1/Documents/data_collection/tiff_06-10-2024'
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
slice_nbr = 0
doFrameCount = False

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
t_list = []
direction_list = []
slice_nbr_list = []
mins_list = []

for i in range(0, nbr_files):
    # Open image and extract stack size
    im = ski.io.imread(stack_files[i], dtype=np.uint16)
    # check stack is 200 slices
    if im.shape[0] >= slice_nbr or doFrameCount == False:
        print('Correct slide number in file')
        
        if doFrameCount == True:
            slice_nbr = im.shape[0]
        else:
            slice_nbr = 1

        # get path and ID
        image_full_path = stack_files[i]
        image_name = os.path.splitext(os.path.basename(stack_files[i]))[0]
        print(image_name)
        image_id = image_name.split('_')[0].zfill(3)
        #protocol = '_'.join(image_full_path.split('\\')[1].split(' ')[0:2])
        protocol = 'long_term_drift'

        # get x , y and z values
        coordinate_string = image_name.replace(image_id + "_", "").replace("_", "")
        x = int(re.split(r'[xyztm]', coordinate_string)[1])
        y = int(re.split(r'[xyztm]', coordinate_string)[2])
        z = int(re.split(r'[xyztm]', coordinate_string)[3])
        if(len(re.split(r'[xyztm]', coordinate_string))>4):
            t = int(re.split(r'[xyztm]', coordinate_string)[4])
        else:
            t = 0
        
        #Take custom minute values
        if(len(re.split(r'[xyztm]', coordinate_string))>5):
            minutes = int(re.split(r'[xyztm]', coordinate_string)[5])
            mins_list.append(minutes)

        print("ID = ", image_id, ", X = ", x,
               ", Y = ", y, ", Z = ", z, ", t = ", t)

        # Append all variable to lists
        path_list.append(image_full_path)
        image_name_list.append(image_name)
        protocol_list.append(protocol)
        id_list.append(image_id)
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
        t_list.append(t)
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
coord_table['X_input_microm'] = x_list
coord_table['Y_input_microm'] = y_list
coord_table['Z_input_microm'] = z_list
coord_table['t'] = t_list


if len(mins_list) < 1:
    # add the actual time in minutes
    #define conditions
    conditions = [
        (coord_table['t'] == 0),
        (coord_table['t'] == 1),
        (coord_table['t'] == 2),
        (coord_table['t'] == 3),

    ]
    #define results
    results = [0, 30, 60, 120]

    #create new column based on conditions in column1 and column2
    coord_table['Time_in_min'] = np.select(conditions, results)
else:
    coord_table['Time_in_min'] = mins_list


# Add a direction columns indicating the sign and axis of the movement

for i in range(0, len(coord_table)):
    d_str = ''
    if coord_table['X_input_microm'][i] == 0 and coord_table['Y_input_microm'][i] == 0:
        d_str += 'Zero'
    
    if coord_table['X_input_microm'][i] < 0:
        d_str += 'X_negative'
    
    if coord_table['X_input_microm'][i] > 0:
        d_str += 'X_positive'
    
    if coord_table['Y_input_microm'][i] < 0:
        d_str += 'Y_negative'
    
    if coord_table['Y_input_microm'][i] > 0:
        d_str += 'Y_positive'
    
    direction_list.append(d_str)

coord_table['Direction'] = direction_list

# Sort table by Y values, X value and time
coord_table = coord_table.sort_values(['ID', 'X_input_microm', 'Y_input_microm', 't', 'Direction'],
                            ascending=[True, True, True, True, True])

# save table as .csv
current_time = datetime.now().strftime("%Y_%m_%d-%p%I_%M_%S")
coord_table.to_csv(path_or_buf=output_path + '/Theoretical_coordinates_table_drift_' + current_time + '.csv',
                   sep=',',
                   na_rep='NA',
                   header=True,
                   index=False,
                   encoding='utf-8-sig')
print(f'Coordinates table saved as csv : {output_path}/Theoretical_coordinates_table_drift.csv')