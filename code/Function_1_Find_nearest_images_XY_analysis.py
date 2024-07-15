"""
Created on 28 May 2024
@author: Estelle

Functions used with "S1_Get_table_of_coordinates_XY_analysis.py"

"""

# Import basic necessary packages/functions
import numpy as np

# Define a function that splits the dataframe into the different protocols
# For each protocol, retrieve the path of the nearest image at location (0,0,0) before and after each translation image
# LIMITATIONS : finding the nearest (0;0;0) will not work in some cases of files misnaming such as :
#   - if more than 2 files have the same ID
#   - if more than 3 files in a row are missing (for e.g. if 3 errors in a row)

def find_nearest_zero(protocol):
    # Create a table that contains only the images at (0,0,0)
    protocol_zeros = protocol.loc[
        (protocol['X_input_steps'] == 0) & (protocol['Y_input_steps'] == 0)].reset_index(drop=True)
    # Add two empty columns to retrieve the path of the nearest zeros before and after the file of interest
    protocol["Path_zero_before"] = np.nan
    protocol["Path_zero_after"] = np.nan
    # Loop through table and identify the nearest (0,0,0) before and after
    for k in range(0, len(protocol)):
        if (protocol['X_input_steps'][k] != 0) or (protocol['Y_input_steps'][k] != 0):
            print("image ID = ", protocol['ID'][k], "; Y displacement = ", protocol['X_input_steps'][k],
                  "; Y displacement = ", protocol['Y_input_steps'][k])
            # Identify the closest neighbours
            nearest = protocol_zeros.iloc[
                (protocol_zeros['Numeric_id'] - protocol['Numeric_id'][k]).abs().argsort()[:2]]
            print(nearest.to_string())
            # Get both before and after images path and fill in the appropriate cell in the table
            path_before = nearest.loc[nearest['Numeric_id'] == min(nearest['Numeric_id']), 'Image_path'].item()
            path_after = nearest.loc[nearest['Numeric_id'] == max(nearest['Numeric_id']), 'Image_path'].item()
            protocol.iloc[k, protocol.columns.get_loc("Path_zero_before")] = path_before
            protocol.iloc[k, protocol.columns.get_loc("Path_zero_after")] = path_after
    return protocol
