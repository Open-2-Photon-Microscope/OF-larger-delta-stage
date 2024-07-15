"""
Created on 30 May 2024
@author: Estelle

This scripts creates summary plots for the translation in X, Y or XY.

--> INPUT = table of coordinates containing the translation results
            (obtained from "S3_Align_with_skimage_cross_correlation_XY_analysis.py")
--> OUTPUT1 = several plots for each protocol :
    PROTOCOL 1 : UNIDIRECTIONAL TRANSLATION
        1 - Protocol_1_Theoretical_vs_recorded_translation.png = Shows the lines of theoretical movement opposed to the actual recorded distance as dots
        2 - Protocol_1_X_translation_error.png  = amount of error in X movement depending on the theoretical direction and distance
        3 - Protocol_1_Y_translation_error.png =  amount of error in Y movement depending on the theoretical direction and distance
        4 - Protocol_1_Going_back_to_Zero_translation_error.png = Recorded difference between the images at (0;0) before and after the translation was made
    PROTOCOL 2 : BIDIRECTIONAL TRANSLATION
        5 - Protocol_2_Theoretical_vs_recorded_translation.png = Shows the lines of theoretical movement opposed to the actual recorded distance as dots
        6 - Protocol_2_Going_back_to_Zero_translation_error.png = Recorded difference between the images at (0;0) before and after the translation was made
--> OUTPUT2 = a statistical summary containing the mean and sd for each error in the x and y axis, for x or y or x and y translation

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


                                    #####################
                                    #### PROTOCOL 1 #####
                                    #####################

# Create a statistic summary table for protocol 1
stat_table_protocol_1 = coord[(coord['Direction'].notna()) & (coord['Protocol'] == 'Protocol_1')]
stat_table_protocol_1 = stat_table_protocol_1.rename(columns={'Crosscor_tx_microm': 'xt',
                                                              'Crosscor_ty_microm': 'yt',
                                                              'X_input_microm' : 'X_input',
                                                              'Y_input_microm': 'Y_input'})
stat_table_protocol_1 = stat_table_protocol_1[["X_input", "Y_input", "Direction", "xt", "yt"]]
# Calculate error for each image
stat_table_protocol_1['Error_X'] = abs(stat_table_protocol_1['X_input'])-abs(stat_table_protocol_1['xt'])
stat_table_protocol_1['Error_Y'] = abs(stat_table_protocol_1['Y_input'])-abs(stat_table_protocol_1['yt'])


stat_table_protocol_1 = stat_table_protocol_1.iloc[1:].reset_index() # remove first row (initial 0)
stat_table_protocol_1['ID'] = stat_table_protocol_1.index//2
stat_table_protocol_1 = stat_table_protocol_1.reset_index()
stat_table_protocol_1 = pd.melt(stat_table_protocol_1, id_vars=['ID', 'X_input', 'Y_input', 'Direction'],
                                value_vars=['Error_X', 'Error_Y'],
                                value_name='Absolute_error_microm',
                                var_name='Error_type')

stat_table_protocol_1['Error_type'].loc[stat_table_protocol_1['Direction'] == 'Zero'] = stat_table_protocol_1['Error_type']+ "_back_to_0"
stat_table_protocol_1['Error_type'].loc[stat_table_protocol_1['Direction'] != 'Zero'] = stat_table_protocol_1['Error_type']+ "_during_translation"

stat_table_protocol_1 = stat_table_protocol_1.replace(to_replace='Zero', method="ffill")

stat_table_protocol_1 = stat_table_protocol_1.groupby('ID').filter(lambda x: ((abs(x['X_input']).max())<200) & ((abs(x['Y_input']).max())<200))
stat_table_protocol_1.reset_index(drop=True, inplace=True) # reset index

# Create boxplot comparing the error values for each category

fig, ax = plt.subplots(figsize=(12, 6))
p = sns.boxplot(x = stat_table_protocol_1['Direction'],
            y = stat_table_protocol_1['Absolute_error_microm'],
            hue = stat_table_protocol_1['Error_type'],
            showmeans=True,
            meanprops={'marker':'o','markerfacecolor':'black','markeredgecolor':'black','markersize':'7'})
fig.suptitle('Absolute error recorded depending on movement direction', fontsize=14)
plt.savefig(dirname(coord_path)+"/Protocol_1_Error_in_each_group.png")

# Calculate mean and sd values per group and save table of stats
stat_table_protocol_1 = stat_table_protocol_1[["Direction", "Error_type", "Absolute_error_microm"]]

stat_table_protocol_1 = stat_table_protocol_1.groupby(['Direction', 'Error_type']).agg([np.mean, np.std])
stat_table_protocol_1.columns = stat_table_protocol_1.columns.map("_".join)
stat_table_protocol_1 = stat_table_protocol_1.reset_index()

stat_table_protocol_1.to_csv(dirname(coord_path) + "/Protocol_1_statistical_summary.csv", index=False)


# For protocol 1 : TRANSLATION IN ONE DIRECTION ONLY
# Add a column containing the theoretical displacement in either direction
coord_1 = coord[coord['Protocol'] == 'Protocol_1']
coord_1['theoretical_distance'] = (coord_1['X_input_microm']
                                 + coord_1['Y_input_microm'])
coord_1 = coord_1.astype({'theoretical_distance': 'float'})


# Create graphs
plot_coord = coord_1.dropna(subset=['Direction'])
# Plot graphs of recorded vs expected X and Y in each direction
plot_coord = plot_coord[(coord_1['Direction'] != 'Zero')]
plot_coord = plot_coord[(plot_coord['theoretical_distance'] < 300) & (plot_coord['theoretical_distance'] > -300)]

# Plot theoretical vs actual displacement
fig, ax = plt.subplots(figsize=(12, 6))
p2 = sns.lineplot(data=plot_coord, x='X_input_microm', y='Y_input_microm', hue='Direction', ax=ax, legend=None, alpha= 1)

p1 = sns.scatterplot(x="Crosscor_tx_microm",
                    y="Crosscor_ty_microm",
                    hue="Direction",
                    data=plot_coord)

ax.set(xlabel='X Displacement (µm)',
        ylabel='Y Displacement (µm)')
fig.suptitle('Recorded translation in X or Y (dots) compared to theoretical displacement (lines)', fontsize=14)
plt.show()
plt.savefig(dirname(coord_path)+"/Protocol_1_Theoretical_vs_recorded_translation.png")

# Plot X results
plot_x = sns.lmplot(x="theoretical_distance", y="Crosscor_tx_microm", hue="Direction", data=plot_coord,
                    height=6, aspect=1, ci=False)
plot_x.fig.suptitle("X DISPLACEMENT", fontsize=12)
plot_x.set(xlabel="Theoretical movement (µm)",
           ylabel="Recorded X movement (µm)",
           xlim=(-130, 130),
           ylim=(-130, 130))
plt.axvline(0, ymin=0.1, ymax=0.9, color="black", linestyle="--")
plt.axhline(0, xmin=0.1, xmax=0.9, color="black", linestyle="--")
plt.show()
plt.savefig(dirname(coord_path)+"/Protocol_1_X_translation_error.png")

# Plot Y results
plot_y = sns.lmplot(x="theoretical_distance", y="Crosscor_ty_microm", hue="Direction", data=plot_coord,
                    height=6, aspect=1, ci=False)
plot_y.fig.suptitle("Y DISPLACEMENT", fontsize=12)
plot_y.set(xlabel="Theoretical movement (µm)",
           ylabel="Recorded Y movement (µm)",
           xlim=(-130, 130),
           ylim=(-130, 130))
plt.axvline(0, ymin=0.1, ymax=0.9, color="black", linestyle="--")
plt.axhline(0, xmin=0.1, xmax=0.9, color="black", linestyle="--")
plt.show()
plt.savefig(dirname(coord_path)+"/Protocol_1_Y_translation_error.png")

# Plot returning to Zero error
plot_coord_0 = coord_1.dropna(subset=['Direction'])
plot_coord_0 = plot_coord_0.reset_index()
plot_coord_0 = plot_coord_0[(plot_coord_0.theoretical_distance > 0).idxmax():]
plot_coord_0.loc[:, 'Previous_distance'] = plot_coord_0.theoretical_distance.shift(1)
plot_coord_0.loc[:, 'Previous_direction'] = plot_coord_0.Direction.shift(1)
plot_coord_0 = plot_coord_0[plot_coord_0['theoretical_distance'] == 0]
# print(plot_coord_0.to_string())

# Set figure grid
fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=False, figsize=(12, 6))
# Plot X results
sns.scatterplot(x='Previous_distance',
                y='Crosscor_tx_microm',
                hue='Previous_direction',
                data=plot_coord_0,
                ax=ax1)
ax1.set(title='Error in X at Zero location',
        xlabel='Previous theoretical movement (µm)',
        ylabel='Recorded X movement (µm)')
ax1.get_legend().remove()
ax1.axvline(0, ymin=0.1, ymax=0.9, color="black", linestyle="--")
ax1.axhline(0, xmin=0.1, xmax=0.9, color="black", linestyle="--")
# Plot Y results
sns.scatterplot(x="Previous_distance",
                y="Crosscor_ty_microm",
                hue="Previous_direction",
                data=plot_coord_0,
                ax=ax2)
ax2.set(title='Error in Y at Zero location',
        xlabel='Previous theoretical movement (µm)',
        ylabel='Recorded Y movement (µm)')
#sns.move_legend(ax2, "upper left", bbox_to_anchor=(0.5, 1))
ax2.axvline(0, ymin=0.1, ymax=0.9, color="black", linestyle="--")
ax2.axhline(0, xmin=0.1, xmax=0.9, color="black", linestyle="--")
plt.show()
plt.savefig(dirname(coord_path)+"/Protocol_1_Going_back_to_Zero_translation_error.png")

                                    #####################
                                    #### PROTOCOL 2 #####
                                    #####################

# Create a statistic summary table for protocol 2
stat_table_protocol_2 = coord[(coord['Direction'].notna()) & (coord['Protocol'] == 'Protocol_2')]
stat_table_protocol_2 = stat_table_protocol_2.rename(columns={'Crosscor_tx_microm': 'xt',
                                                              'Crosscor_ty_microm': 'yt',
                                                              'X_input_microm' : 'X_input',
                                                              'Y_input_microm': 'Y_input'})
stat_table_protocol_2 = stat_table_protocol_2[["X_input", "Y_input", "Direction", "xt", "yt"]]
# Calculate error for each image
stat_table_protocol_2['Error_X'] = abs(stat_table_protocol_2['X_input'])-abs(stat_table_protocol_2['xt'])
stat_table_protocol_2['Error_Y'] = abs(stat_table_protocol_2['Y_input'])-abs(stat_table_protocol_2['yt'])


stat_table_protocol_2 = stat_table_protocol_2.iloc[1:].reset_index() # remove first row (initial 0)
stat_table_protocol_2['ID'] = stat_table_protocol_2.index//2
stat_table_protocol_2 = stat_table_protocol_2.reset_index()
stat_table_protocol_2 = pd.melt(stat_table_protocol_2, id_vars=['ID', 'X_input', 'Y_input', 'Direction'],
                                value_vars=['Error_X', 'Error_Y'],
                                value_name='Absolute_error_microm',
                                var_name='Error_type')

stat_table_protocol_2['Error_type'].loc[stat_table_protocol_2['Direction'] == 'Zero'] = stat_table_protocol_2['Error_type']+ "_back_to_0"
stat_table_protocol_2['Error_type'].loc[stat_table_protocol_2['Direction'] != 'Zero'] = stat_table_protocol_2['Error_type']+ "_during_translation"

stat_table_protocol_2 = stat_table_protocol_2.replace(to_replace='Zero', method="ffill")

stat_table_protocol_2 = stat_table_protocol_2.groupby('ID').filter(lambda x: ((abs(x['X_input']).max())<200) & ((abs(x['Y_input']).max())<200))
stat_table_protocol_2.reset_index(drop=True, inplace=True) # reset index

# Create boxplot comparing the error values for each category

fig, ax = plt.subplots(figsize=(12, 6))
p = sns.boxplot(x = stat_table_protocol_2['Direction'],
            y = stat_table_protocol_2['Absolute_error_microm'],
            hue = stat_table_protocol_2['Error_type'],
            showmeans=True,
            meanprops={'marker':'o','markerfacecolor':'black','markeredgecolor':'black','markersize':'7'})
fig.suptitle('Absolute error recorded depending on movement direction', fontsize=14)
plt.savefig(dirname(coord_path)+"/Protocol_2_Error_in_each_group.png")

# Calculate mean and sd values per group and save table of stats
stat_table_protocol_2 = stat_table_protocol_2[["Direction", "Error_type", "Absolute_error_microm"]]

stat_table_protocol_2 = stat_table_protocol_2.groupby(['Direction', 'Error_type']).agg([np.mean, np.std])
stat_table_protocol_2.columns = stat_table_protocol_2.columns.map("_".join)
stat_table_protocol_2 = stat_table_protocol_1.reset_index()

stat_table_protocol_2.to_csv(dirname(coord_path) + "/Protocol_2_statistical_summary.csv", index=False)

# For protocol 2 : TRANSLATION IN BOTH DIRECTION

# Add a column containing the theoretical displacement in either direction
coord_2 = coord[coord['Protocol'] == 'Protocol_2']

# Create graphs
coord_2 = coord_2.dropna(subset=['Direction'])
# Plot graphs of recorded vs expected X and Y in each direction
plot_coord = coord_2[(coord_2['Direction'] != 'Zero')]

# Plot theoretical vs actual displacement
fig, ax = plt.subplots(figsize=(12, 6))
p1 = sns.scatterplot(x="Crosscor_tx_microm",
                    y="Crosscor_ty_microm",
                    hue="Direction",
                    data=plot_coord)
p2 = sns.lineplot(data=plot_coord, x='X_input_microm', y='Y_input_microm', hue='Direction', ax=ax, legend=None)
ax.axvline(0, ymin=0.1, ymax=0.9, color="black", linestyle="--")
ax.axhline(0, xmin=0.1, xmax=0.9, color="black", linestyle="--")
ax.set(xlabel='X Displacement (µm)',
        ylabel='Y Displacement (µm)')
fig.suptitle('Recorded translation in XY (dots) compared to theoretical displacement (lines)', fontsize=14)
plt.savefig(dirname(coord_path)+"/Protocol_2_Theoretical_vs_recorded_translation.png")


# Plot returning to Zero error
plot_coord_0 = coord_2.reset_index()
plot_coord_0 = plot_coord_0[(plot_coord_0.Direction != 'Zero').idxmax():]
plot_coord_0.loc[:, 'Previous_x_distance'] = plot_coord_0.X_input_microm.shift(1)
plot_coord_0.loc[:, 'Previous_y_distance'] = plot_coord_0.Y_input_microm.shift(1)
plot_coord_0.loc[:, 'Previous_direction'] = plot_coord_0.Direction.shift(1)
plot_coord_0 = plot_coord_0[plot_coord_0['Direction'] == 'Zero']
# print(plot_coord_0.to_string())

# Set figure grid
fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=False, figsize=(12, 6))
sns.scatterplot(x='Previous_x_distance',
                y='Crosscor_tx_microm',
                hue='Previous_direction',
                data=plot_coord_0,
                ax=ax1)
ax1.set(title='Error in X at Zero location',
        xlabel='Previous theoretical X movement (µm)',
        ylabel='Recorded X movement (µm)')
ax1.get_legend().remove()
ax1.axvline(0, ymin=0.1, ymax=0.9, color="black", linestyle="--")
ax1.axhline(0, xmin=0.1, xmax=0.9, color="black", linestyle="--")
# Plot Y results
sns.scatterplot(x="Previous_y_distance",
                y="Crosscor_ty_microm",
                hue="Previous_direction",
                data=plot_coord_0,
                ax=ax2)
ax2.set(title='Error in Y at Zero location',
        xlabel='Previous theoretical Y movement (µm)',
        ylabel='Recorded Y movement (µm)')
#sns.move_legend(ax2, "upper left", bbox_to_anchor=(0.5, 1))
ax2.axvline(0, ymin=0.1, ymax=0.9, color="black", linestyle="--")
ax2.axhline(0, xmin=0.1, xmax=0.9, color="black", linestyle="--")
plt.show()
plt.savefig(dirname(coord_path)+"/Protocol_2_Going_back_to_Zero_translation_error.png")
