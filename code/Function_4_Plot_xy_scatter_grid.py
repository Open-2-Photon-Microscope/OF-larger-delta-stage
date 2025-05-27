# 3x3 scatter plots showing dx and dy

import pandas as pd
import matplotlib.pyplot as plt

def drift_plot_grid(df:pd.DataFrame):
    set_of_directions = set(df['Direction'].to_list())
    print('List of directions: ',set_of_directions)

    for direction in set_of_directions:
        df.plot.scatter(x='Crosscor_tx_px',y='Crosscor_ty_px')
        plt.show()