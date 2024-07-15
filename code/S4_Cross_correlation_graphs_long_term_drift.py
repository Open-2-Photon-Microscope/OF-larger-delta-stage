"""
Created on 30 May 2024
@author: Estelle

This scripts creates summary plots for the translation in X, Y or XY.

--> INPUT = table of coordinates containing the translation results
            (obtained from "S3_Align_with_skimage_cross_correlation_long_term_drift.py")
--> OUTPUT1 = plots:
        1 - Long_term_drift_absolute_error_in_Y_vs_time.png = absolute error in Y across time
        2 - Long_term_drift_absolute_error_in_X_vs_time.png = absolute error in X across time
"""

# import the necessary packages
import os
from os.path import dirname
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename  # User input interface

# to use this script on its own give the path of coordinates file
# Get main path
outer_dir = dirname(os.getcwd())
# Ask user the path to coordinates file :
root = Tk()
root.attributes("-topmost", True)
root.withdraw()
coord_path = askopenfilename(initialdir=outer_dir, title='Select coordinate file to analyse')
coord = pd.read_csv(coord_path, encoding='utf-8-sig')

# correct the Y values as the cross correlation translation records it the opposite way :
coord['Crosscor_ty_microm'] = - coord['Crosscor_ty_microm']

# Create boxplot comparing the error values for each location tested

fig, ax = plt.subplots(figsize=(12, 6))
p = sns.lineplot(x = coord['Time_in_min'],
                y = abs(coord['Crosscor_ty_microm']),
                hue = coord['Direction'],
                marker="o",
                markersize=10)
fig.suptitle('Absolute error in Y over time', fontsize=14)
plt.savefig(dirname(coord_path)+"/Long_term_drift_absolute_error_in_Y_vs_time.png")

fig, ax = plt.subplots(figsize=(12, 6))
p = sns.lineplot(x = coord['Time_in_min'],
                y = abs(coord['Crosscor_tx_microm']),
                hue = coord['Direction'],
                marker="o",
                markersize=10)
fig.suptitle('Absolute error in X over time', fontsize=14)
plt.savefig(dirname(coord_path)+"/Long_term_drift_absolute_error_in_X_vs_time.png")

