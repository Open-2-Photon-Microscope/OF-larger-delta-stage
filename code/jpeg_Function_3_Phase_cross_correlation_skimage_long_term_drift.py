"""
Created on 28 May 2024
@author: Estelle

Functions used with "S3_Align_with_skimage_cross_correlation_long_term_drift.py"

1- Identify the translation files at each time (t0, t1, t2, t3) and compare each t to the image at t0
2 - Compute a rigid transformation (without depth, only translation) using skimage
See link below for details :
https://scikit-image.org/docs/stable/auto_examples/registration/plot_register_translation.html
3 - Outputs the shift (tx, ty) in pixels and microns

"""


# import the necessary packages
import matplotlib.pyplot as plt
import numpy as np
import cv2
# Import the scikit-image package https://scikit-image.org/
# which allows loading stacks into numpy 3D arrays and use cross correlation to register images
import skimage as ski
from skimage.registration import phase_cross_correlation


# Compute a rigid transformation (without depth, only translation)
# Gives a shift (tx, ty)

def cross_correlation_drift(coord, px_size):
    image_list = []
    # Find and read image at t0
    direction = coord['Direction'][0]
    distance = "(" + str(int(coord['X_input_microm'][0])) + ";" + str(int(coord['Y_input_microm'][0])) + ")"
    t0_path = coord.loc[coord['t']==0, 'Image_path'].item()
    t0_image = cv2.imread(t0_path)
    t0_image = cv2.cvtColor(t0_image, cv2.COLOR_BGR2GRAY)
    image_list.append(t0_image)

    # Get image dimensions
    height, width = t0_image.shape

    # Loop through coordinate file and retrieve other time data
    for i in range(1, len(coord)):
        time_path = coord.loc[coord['t']==i, 'Image_path'].item()
        print(time_path)
        time_image = cv2.imread(time_path)
        time_image = cv2.cvtColor(time_image, cv2.COLOR_BGR2GRAY)
        # Calculate cross correlation and extract shift values
        shift_t0_t1, error, diffphase = phase_cross_correlation(t0_image, time_image, upsample_factor=100)

        # Store translation values in pixel in lists
        tx = shift_t0_t1[1]
        ty = shift_t0_t1[0]

        # Compute a euclidian transformation matrix
        transformation_matrix = np.array([[1, -0, tx], [0, 1, ty]])
        # Apply transformation to images
        transformed_img = cv2.warpAffine(time_image, transformation_matrix, (width, height),
                                        borderValue=(150, 0, 0)
                                        )
        # Save the output.
        # Convert back to a 16bits image
        transformed_img = ski.util.img_as_uint(transformed_img)
        image_list.append(transformed_img)

        # Save translation values
        coord.loc[i, 'Crosscor_tx_px'] = tx
        coord.loc[i, 'Crosscor_ty_px'] = ty
        coord['Crosscor_tx_microm'] = coord.Crosscor_tx_px * px_size
        coord['Crosscor_ty_microm'] = coord.Crosscor_ty_px * px_size

    # plot
    fig = plt.figure(figsize=(15, 6))
    fig.suptitle(f"Cross correlation of the drift a different time at location {distance} ({direction}) ",
                 fontsize=16)
    ax0 = plt.subplot(1, len(coord), 1)
    ax0.imshow(image_list[0], cmap='inferno')
    ax0.set_axis_off()
    ax0.set_title('T0 = 0')
    plt.show()

    for i in range(1,len(coord)):
        txt_y = round(0.30-(i*0.05),2)
        plt.figtext(x=0.15, y=txt_y,
                    s=f"Detected translation in µm (y, x) at {coord['Time_in_min'][i]} min: ({round(coord.Crosscor_ty_microm.values[i], 2)}; "
                    f"{round(coord.Crosscor_tx_microm.values[i], 2)})",
                    horizontalalignment='left',
                    fontsize=12)
        ax_i = plt.subplot(1, len(coord), i+1, sharex=ax0, sharey=ax0)
        ax_i.imshow(image_list[i], cmap='inferno')
        ax_i.set_axis_off()
        ax_i.set_title(f"T{i} = {coord['Time_in_min'][i]} min")
        ax_i.patch.set_linewidth(1)
        plt.show()

        # plt.close()
        # return the translation coordinates and plots
    return coord, fig
