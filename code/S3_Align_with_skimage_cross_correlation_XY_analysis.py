# -*- coding: utf-8 -*-
"""
Created on 30 May 2024
@author: Estelle

Script used to compute a rigid transformation (without depth, only scale + rotation + translation) on the

It uses a function defined in "Function_3_Phase_cross_correlation_skimage_XY_analysis.py"

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
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename  # User input interface

# Import relevant functions from other scripts
from Function_3_Phase_cross_correlation_skimage_XY_analysis import cross_correlation_xy

# Fixed variables
px_size = 1/0.512
plot_nbr = 0

# Get main path
outer_dir = dirname(os.getcwd())
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

# X and Y analysis
for i in range(0, len(coord_table)):
    if (coord_table['X_input_steps'][i] != 0) or (coord_table['Y_input_steps'][i] != 0):
        protocol = coord_table['Protocol'][i]
        # Add comparison ID number and define plot output name
        plot_nbr += 1
        plot_id = str(plot_nbr).zfill(3)
        plot_path = (f"{output_path}/{protocol}/{plot_id}_Registration_y{int(coord_table['Y_input_microm'][i])}"
                     f"_x{int(coord_table['X_input_microm'][i])}_cross_corr.png")

        # Compute a rigid transformation (without depth, only scale + rotation + translation)
        coord, full_plot = cross_correlation_xy(i=i, coord=coord_table, px_size=px_size)
        full_plot.savefig(plot_path)

coord.to_csv(output_path + "/Coord_table_cv2_cross_correlation.csv", index=False)
