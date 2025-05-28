import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

# Dummy data per "Direction" cell
def generate_data(seed=0):
    np.random.seed(seed)
    x = np.random.normal(loc=0, scale=1, size=300)
    y = np.random.normal(loc=0, scale=1, size=300)
    return x, y

fig = plt.figure(figsize=(12, 12))
outer = GridSpec(3, 3, wspace=0.5, hspace=0.5)

for i in range(3):
    for j in range(3):
        # Create inner GridSpec: 2 rows, 2 columns
        gs = GridSpecFromSubplotSpec(2, 2, width_ratios=[4, 1], height_ratios=[1, 4], 
                      wspace=0.0, hspace=0.0, 
                      subplot_spec=outer[i, j])  # << attach to outer grid

        # Axes
        ax_main = fig.add_subplot(gs[1, 0])
        ax_histx = fig.add_subplot(gs[0, 0], sharex=ax_main)
        ax_histx.axis('off')
        ax_histy = fig.add_subplot(gs[1, 1], sharey=ax_main)
        ax_histy.axis('off')

        # Sample data
        x, y = generate_data(seed=i*3+j)

        # Plot
        ax_main.scatter(x, y, alpha=0.3, s=10)
        ax_histx.hist(x, bins=30, color='gray')
        ax_histy.hist(y, bins=30, orientation='horizontal', color='gray')

        # Hide labels/ticks for histograms
        ax_histx.tick_params(labelbottom=False)
        ax_histy.tick_params(labelleft=False)

        # Optionally: set same limits across all
        ax_main.set_xlim(-4, 4)
        ax_main.set_ylim(-4, 4)
        ax_histx.set_xlim(-4, 4)
        ax_histy.set_ylim(-4, 4)

plt.tight_layout()
plt.show()
