# import the necessary packages
import os
from os.path import dirname
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
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


# Create graphs
plot_coord = coord.dropna(subset=['Direction'])
# Plot graphs of recorded vs expected X and Y in each direction
plot_coord = plot_coord[(coord['Direction'] != 'Zero') &
                        (coord['Direction'] != 'Z_positive') &
                        (coord['Direction'] != 'Z_negative')]
plot_coord = plot_coord[(plot_coord['theoretical_distance'] < 300) & (plot_coord['theoretical_distance'] > -300)]

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
plt.savefig(dirname(coord_path)+"/X_translation_error.png")

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
plt.savefig(dirname(coord_path)+"/Y_translation_error.png")

# Plot returning to Zero error
plot_coord_0 = coord.dropna(subset=['Direction'])
plot_coord_0 = plot_coord_0[(plot_coord_0['Direction'] != 'Z_positive') &
                            (plot_coord_0['Direction'] != 'Z_negative')]
plot_coord_0 = plot_coord_0.reset_index()
plot_coord_0 = plot_coord_0[(plot_coord_0.theoretical_distance > 0).idxmax():]
plot_coord_0.loc[:, 'Previous_distance'] = plot_coord_0.theoretical_distance.shift(1)
plot_coord_0.loc[:, 'Previous_direction'] = plot_coord_0.Direction.shift(1)
plot_coord_0 = plot_coord_0[plot_coord_0['theoretical_distance'] == 0]
# print(plot_coord_0.to_string())

# Set figure grid
fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=True, figsize=(12, 6))
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
sns.move_legend(ax2, "upper left", bbox_to_anchor=(0.5, 1))
ax2.axvline(0, ymin=0.1, ymax=0.9, color="black", linestyle="--")
ax2.axhline(0, xmin=0.1, xmax=0.9, color="black", linestyle="--")
plt.show()
plt.savefig(dirname(coord_path)+"/Zero_translation_error.png")
