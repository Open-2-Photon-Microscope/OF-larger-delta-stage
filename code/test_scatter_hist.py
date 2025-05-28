import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

def grid_plot(df: pd.DataFrame, xrange=11, yrange=11):
    groups = df.groupby('Direction')

    direction_positions = {
        'X_negative_Y_positive': (0, 0),
        'Y_positive':            (0, 1),
        'X_positive_Y_positive': (0, 2),
        'X_negative':            (1, 0),
        'Zero':                  (1, 1),
        'X_positive':            (1, 2),
        'X_negative_Y_negative': (2, 0),
        'Y_negative':            (2, 1),
        'X_positive_Y_negative': (2, 2),
    }

    fig = plt.figure(figsize=(12, 12))
    outer = GridSpec(3, 3, wspace=0.6, hspace=0.6)

    for direction, (i, j) in direction_positions.items():
        if direction not in groups.groups:
            continue

        sub_df = groups.get_group(direction)
        x = sub_df['Crosscor_tx_px']
        y = sub_df['Crosscor_ty_px']

        # Create nested grid for each subplot (scatter + histograms)
        inner = GridSpecFromSubplotSpec(
            2, 2, width_ratios=[4, 1], height_ratios=[1, 4],
            wspace=0.0, hspace=0.0,
            subplot_spec=outer[i, j]
        )

        ax_main = fig.add_subplot(inner[1, 0])
        ax_histx = fig.add_subplot(inner[0, 0], sharex=ax_main)
        ax_histx.axis('off')
        ax_histy = fig.add_subplot(inner[1, 1], sharey=ax_main)
        ax_histy.axis('off')

        # Plot scatter
        ax_main.scatter(x, y, alpha=0.3, s=10)

        # Marginal histograms
        ax_histx.hist(x, bins=30, color='gray')
        ax_histy.hist(y, bins=30, orientation='horizontal', color='gray')

        # Hide axis labels for marginals
        ax_histx.tick_params(labelbottom=False)
        ax_histy.tick_params(labelleft=False)

        # Consistent limits
        ax_main.set_xlim(-xrange, xrange)
        ax_main.set_ylim(-yrange, yrange)
        ax_histx.set_xlim(-xrange, xrange)
        ax_histy.set_ylim(-yrange, yrange)

        # Optional: Title
        ax_main.text(
                0.5, -0.15,
                direction,
                ha='center', va='top',
                transform=ax_main.transAxes,
                fontsize=10
            )

    plt.tight_layout()
    plt.show()
