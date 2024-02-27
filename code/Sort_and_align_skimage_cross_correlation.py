# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 09:41:37 2024
@author: estel
"""

# Import basic necessary packages/functions
import os
from os.path import dirname
import pandas as pd
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askdirectory  # User input interface

# Import relevant functions from other scripts
from Registration_cross_correlation import cross_correlation_xy

# Fixed variables
px_size = 1/0.512
plot_nbr = 0

# Get main path
outer_dir = dirname(os.getcwd())
# Ask user the path to Z projected data
root = Tk()
root.attributes("-topmost", True)
root.withdraw()
img_path = askdirectory(initialdir=outer_dir,
                        title='Select folder containing projected files')
# Create an output directory if it doesn't exist
output_path = dirname(img_path) + "/Align_cross_corr"
os.makedirs(output_path, exist_ok=True)

coord = pd.read_csv(img_path + "/Theoretical_coordinates_table.csv",
                    encoding='utf-8-sig')
np.vstack([coord.columns, coord.values])
# X and Y analysis
for index, row in coord.iterrows():
    if (row['X_input_steps'] != 0) & (row['Y_input_steps'] == 0) & (row['Z_input_steps'] == 0):
        translated_index = int(index)
        # Add comparison ID number and define plot output name
        plot_nbr += 1
        plot_id = str(plot_nbr).zfill(3)
        plot_path = (f"{output_path}/{plot_id}_Registration_y{int(coord.Y_input_microm.values[translated_index])}"
                     f"_x{int(coord.X_input_microm.values[translated_index])}_cross_corr.png")

        # Compute a rigid transformation (without depth, only scale + rotation + translation)
        coord, full_plot = cross_correlation_xy(translated_index, coord, px_size=px_size)
        full_plot.savefig(plot_path)

    if (row['X_input_steps'] == 0) & (row['Y_input_steps'] != 0) & (row['Z_input_steps'] == 0):
        translated_index = int(index)
        # Add comparison ID number and define plot output name
        plot_nbr += 1
        plot_id = str(plot_nbr).zfill(3)
        plot_path = (f"{output_path}/{plot_id}_Registration_y{int(coord.Y_input_microm.values[translated_index])}"
                     f"_x{int(coord.X_input_microm.values[translated_index])}_cross_corr.png")

        # Compute a rigid transformation (without depth, only scale + rotation + translation)
        coord, full_plot = cross_correlation_xy(translated_index, coord, px_size=px_size)
        full_plot.savefig(plot_path)

coord.to_csv(output_path + "/Coord_table_cv2_cross_correlation.csv", index=False)
