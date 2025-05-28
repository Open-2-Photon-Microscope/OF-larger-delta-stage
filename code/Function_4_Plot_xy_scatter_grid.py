# 3x3 scatter plots showing dx and dy

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np

def grid_plot(df:pd.DataFrame, xrange=10,yrange=10):
    groups = df.groupby('Direction')

    direction_positions = {
    'X_negative_Y_positive': (0, 0),
    'Y_positive':           (0, 1),
    'X_positive_Y_positive': (0, 2),
    'X_negative':           (1, 0),
    'Zero':                 (1, 1),
    'X_positive':           (1, 2),
    'X_negative_Y_negative': (2, 0),
    'Y_negative':           (2, 1),
    'X_positive_Y_negative': (2, 2),
}
    fig, axes = plt.subplots(3, 3, figsize=(12,12))

    for direction, (i,j) in direction_positions.items():
        ax = axes[i,j]
        group = df[df['Direction'] == direction]
        ax.scatter(group['Crosscor_tx_px'],group['Crosscor_ty_px'],alpha=1/len(group['Crosscor_tx_px']))
        ax.set_title(direction)
        ax.set_aspect('equal')
        #ax.set_xlim(-xrange,xrange)
        #ax.set_ylim(-yrange,yrange)
        # Add inset histograms
        ax_histx = ax.inset_axes([0,1,1,0.25],sharex=ax)
        ax_histx.hist(group['Crosscor_tx_px'], bins=20, color='gray', alpha=0.6)
        #ax_histx.set_xlim(-xrange,xrange)
        ax_histx.axis('off')

        ax_histy = ax.inset_axes([1,0,0.25,1],sharey=ax)
        ax_histy.hist(group['Crosscor_ty_px'], bins=20, orientation='horizontal', color='gray', alpha=0.6)
        #ax_histy.set_ylim(-yrange,yrange)
        ax_histy.axis('off')
    
    for ax in axes.flatten()[len(groups):]:
        ax.set_visible(False)

    plt.tight_layout()
    plt.show()
