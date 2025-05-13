# -*- coding: utf-8 -*-
"""
Created on 30 May 2024
@author: Estelle

Script used to compute a rigid transformation (without depth, only scale + rotation + translation) on the

It uses a function defined in "Function_3_Phase_cross_correlation_skimage_old.py"

--> INPUT = Table of coordinates containing the path to the Z projected .tiff files
            (obtained from "S2_Z_projection_and_contrast_enhancement.py")
--> OUTPUT1 = Summary plot for each image showing the result of the skimage transformation
            Translations values and theoretical values are given in pixels and microns
--> OUTPUT2 = Saves a new coordinate table containing the translation values in pixels and microns
"""

# Import basic necessary packages/functions
import os
from os.path import dirname
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename  # User input interface

# Import relevant functions from other scripts
from Function_3_Phase_cross_correlation_skimage_long_term_drift import cross_correlation_drift

# Fixed variables
px_size = 1/0.512
plot_nbr = 0

# Get main path
outer_dir = dirname(os.getcwd())
outer_dir = input('Enter path to files: ')
# Ask user the path to the coordinate table (can be for a single protocol or all protocol merged)
root = Tk()
root.attributes("-topmost", True)
root.withdraw()
table_path = askopenfilename(initialdir=outer_dir, title='Select the table of coordinate containing Z projected files paths')
print(table_path)

# Read coordinate table
coord_table = pd.read_csv(table_path)

# Create an output directory if it doesn't exist
output_path = dirname(dirname(table_path)) + "/Align_cross_corr"
os.makedirs(output_path, exist_ok=True)

# Create an output directories if it doesn't exist for each protocol
protocol_name_list = coord_table['Protocol'].unique()
for k in range(0, len(protocol_name_list)):
    protocol_path = output_path + "/" + protocol_name_list[k]
    os.makedirs(protocol_path, exist_ok=True)  # exist_ok set to true to not raise an error if the folder exists

# Drift analysis
direction_list = coord_table['Direction'].unique()
appended_data = []

for i in range(0, len(direction_list)):
    direction = direction_list[i]
    short_table = coord_table[coord_table['Direction'] == direction].reset_index(drop=True)
    protocol = short_table['Protocol'][0]

    # Add comparison ID number and define plot output name
    plot_nbr += 1
    plot_id = str(plot_nbr).zfill(3)
    plot_path = (f"{output_path}/{protocol}/{plot_id}_{direction}_drift.png")

    # Compute a rigid transformation (without depth, only scale + rotation + translation)
    coord, full_plot = cross_correlation_drift(coord=short_table, px_size=px_size)
    full_plot.savefig(plot_path)

    # append df to list
    appended_data.append(coord)


coord_all = pd.concat(appended_data)
coord_all.to_csv(output_path + "/Coord_table_cv2_cross_correlation.csv", index=False)
