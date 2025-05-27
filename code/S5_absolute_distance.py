#calculate absolute distance drifted
import os
import math
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statistics import stdev, mean

def get_hypot(dx,dy):
    hypot = abs(math.sqrt(dx**2 + dy**2))
    return hypot

def plot_nice(df:pd.DataFrame):
    # Clean start
    plt.close('all')

    # Create one figure and one axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Group by 'Direction' and plot each with error bars
    for direction, group in df.groupby('Direction'):
        group = group.sort_values('Time_in_min')
        ax.errorbar(
            group['Time_in_min'],
            group['Mean_px_drift'],
            yerr=group['SE_px_drift'],
            label=direction,
            capsize=3,
            marker='o',
            linestyle='-'
        )

    # Labeling and formatting
    ax.set_xlabel('Time (min)')
    ax.set_ylabel('Mean Pixel Drift')
    ax.set_title('Drift over Time by Direction')
    ax.legend(title='Direction')
    ax.grid(True)

    # Show one final plot
    fig.tight_layout()
    plt.show()

    plt.xlabel('Time (min)')
    plt.ylabel('Mean Pixel Drift')
    plt.title('Drift over Time by Direction')
    plt.legend(title='Direction')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def bplot(df:pd.DataFrame, x='Time_in_min'):
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x=x, y='px_drift')

    plt.xlabel('Time (min)')
    plt.ylabel('Pixel Drift')
    plt.title('Distribution of Pixel Drift by Time')
    plt.xticks(rotation=45)  # Optional: Rotate if too crowded
    plt.tight_layout()
    plt.show()

filename = 'Coord_table_cv2_cross_correlation.csv'

all_data = pd.DataFrame()

# Assign directory
directory = input('Enter parent directory: ')

# Iterate over files in directory
for path, folders, files in os.walk(directory):
    for folder_name in folders:
        if filename in os.listdir(f'{path}/{folder_name}'):
            print(f'Content of {folder_name}')
            with open(f'{path}/{folder_name}/{filename}') as f:
                px_drift = []
                data = pd.read_csv(f)
                print(data)

                for i in range(len(data['Crosscor_tx_px'])):
                    px_drift.append(get_hypot(data['Crosscor_tx_px'][i],data['Crosscor_ty_px'][i]))
                data['px_drift'] = px_drift
                
                all_data = pd.concat([all_data,data]).reset_index(drop=True)
       'Time_in_min'data = all_data[['Direction','Time_in_min','px_drift']].fillna(0)

useful_data.to_csv(f'{directory}/drift_data.csv',index=False)
useful_data.sort_values('Direction')



plot_data = []


direction_set = set(useful_data['Direction'].to_list())
for direction in direction_set:
    
    temp = useful_data[useful_data['Direction']==direction] # temporary df of only specific direction

    # find the mean for each Time_in_min
    for minutes in set(temp['Time_in_min'].to_list()):
        min_data = temp[temp['Time_in_min']==minutes] # temp df of only specific time in mins
        values = min_data['px_drift'].to_list()
        plot_data.append([direction,minutes,mean(values),stdev(values)])

plot_data = pd.DataFrame(plot_data, columns=['Direction','Time_in_min','Mean_px_drift','SE_px_drift'])
plot_data = plot_data.sort_values(['Direction','Time_in_min'])
plot_data.to_csv(f'{directory}/mean_drift_data.csv',index=False)
#plot_nice(plot_data)