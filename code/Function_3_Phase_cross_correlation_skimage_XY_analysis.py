"""
Created on 28 May 2024
@author: Estelle

Functions used with "S3_Align_with_skimage_cross_correlation_XY_analysis.py"

1- Identify the translation file plus the zero before and after
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

def cross_correlation_xy(i, coord, px_size):

    before_path = coord['Path_zero_before'][i]
    translation_path = coord['Image_path'][i]
    after_path = coord['Path_zero_after'][i]

    before_index = coord['Image_path'].str.contains(before_path)
    before_index = before_index[before_index].first_valid_index()
    translated_index = i
    after_index = coord['Image_path'].str.contains(after_path)
    after_index = after_index[after_index].first_valid_index()

    before_image = cv2.imread(before_path)
    translation_image = cv2.imread(translation_path)
    after_image = cv2.imread(after_path)

    before_image = cv2.cvtColor(before_image, cv2.COLOR_BGR2GRAY)
    translation_image = cv2.cvtColor(translation_image, cv2.COLOR_BGR2GRAY)
    after_image = cv2.cvtColor(after_image, cv2.COLOR_BGR2GRAY)

    height, width = before_image.shape

    # Calculate cross correlation and extract shift values
    shift_bt, error, diffphase = phase_cross_correlation(before_image, translation_image, upsample_factor=100)
    shift_ba, error_0, diffphase_0 = phase_cross_correlation(before_image, after_image, upsample_factor=100)

    tx_bt = shift_bt[1]
    ty_bt = shift_bt[0]
    tx_ba = shift_ba[1]
    ty_ba = shift_ba[0]

    # Compute a euclidian transformation matrix
    transformation_matrix_bt = np.array([[1, -0, tx_bt], [0, 1, ty_bt]])
    transformation_matrix_ba = np.array([[1, -0, tx_ba], [0, 1, ty_ba]])

    # Apply transformation to images
    transformed_img_bt = cv2.warpAffine(translation_image, transformation_matrix_bt, (width, height),
                                        borderValue=(150, 0, 0)
                                        )
    transformed_img_ba = cv2.warpAffine(after_image, transformation_matrix_ba, (width, height),
                                        borderValue=(150, 0, 0)
                                        )
    # Save the output.
    # Convert back to a 16bits image
    transformed_img_bt = ski.util.img_as_uint(transformed_img_bt)
    transformed_img_ba = ski.util.img_as_uint(transformed_img_ba)

    # Save translation values
    coord.loc[translated_index, 'Crosscor_tx_px'] = tx_bt
    coord.loc[translated_index, 'Crosscor_ty_px'] = ty_bt
    coord.loc[after_index, 'Crosscor_tx_px'] = tx_ba
    coord.loc[after_index, 'Crosscor_ty_px'] = ty_ba
    coord.loc[translated_index, 'Crosscor_tx_microm'] = tx_bt * px_size
    coord.loc[translated_index, 'Crosscor_ty_microm'] = ty_bt * px_size
    coord.loc[after_index, 'Crosscor_tx_microm'] = tx_ba * px_size
    coord.loc[after_index, 'Crosscor_ty_microm'] = ty_ba * px_size

    if coord['X_input_microm'][i] == 0 and coord['Y_input_microm'][i] == 0:
        dir1 = 'Zero'
    else:
        dir1 = ''
    if coord['X_input_microm'][i] < 0:
        dir2 = 'X_negative'
    else:
        dir2 = ''
    if coord['X_input_microm'][i] > 0:
        dir3 = 'X_positive'
    else:
        dir3 = ''
    if coord['Y_input_microm'][i] < 0:
        dir4 = 'Y_negative'
    else:
        dir4 = ''
    if coord['Y_input_microm'][i] > 0:
        dir5 = 'Y_positive'
    else:
        dir5 = ''
    direction = [dir1, dir2, dir3, dir4, dir5]
    direction = [x for x in direction if x]
    direction = '_'.join(direction)

    coord.loc[before_index, 'Direction'] = 'Zero'
    coord.loc[translated_index, 'Direction'] = direction
    coord.loc[after_index, 'Direction'] = 'Zero'

    # plot
    fig = plt.figure(figsize=(10, 5))
    fig.suptitle(f"Cross correlation Alignment of images {coord.ID.values[before_index]}, "
                 f"{coord.ID.values[translated_index]} "
                 f"and {coord.ID.values[after_index]}",
                 fontsize=16)
    plt.figtext(0.5, 0.85,
                f"Known offset in µm (y, x): ({int(coord.Y_input_microm.values[translated_index])}; "
                f"{int(coord.X_input_microm.values[translated_index])})",
                horizontalalignment='center',
                fontsize=12)
    plt.figtext(0.15, 0.15,
                f"Detected translation in pixels (y, x): ({round(coord.Crosscor_ty_px.values[translated_index], 2)}; "
                f"{round(coord.Crosscor_tx_px.values[translated_index], 2)})",
                horizontalalignment='left',
                fontsize=12)
    plt.figtext(0.15, 0.1,
                f"Detected translation in µm (y, x): ({round(coord.Crosscor_ty_microm.values[translated_index], 2)}; "
                f"{round(coord.Crosscor_tx_microm.values[translated_index], 2)})",
                horizontalalignment='left',
                fontsize=12)
    plt.figtext(0.15, 0.05,
                f"Detected zero offset in pixels (y, x): ({round(coord.Crosscor_ty_px[after_index], 2)}; "
                f"{round(coord.Crosscor_tx_px[after_index], 2)})",
                horizontalalignment='left',
                fontsize=12)
    ax1 = plt.subplot(1, 3, 1)
    ax2 = plt.subplot(1, 3, 2, sharex=ax1, sharey=ax1)
    ax3 = plt.subplot(1, 3, 3, sharex=ax1, sharey=ax1)

    ax1.imshow(before_image, cmap='inferno')
    ax1.set_axis_off()
    ax1.set_title('Reference image')
    ax2.imshow(transformed_img_bt, cmap='inferno')
    ax2.patch.set_linewidth(1)
    ax2.set_axis_off()
    ax2.set_title('Translation')
    ax3.imshow(transformed_img_ba, cmap='inferno')
    ax3.set_axis_off()
    ax3.set_title("Return to 0")
    plt.close()
    # return the translation coordinates and plots
    return coord, fig
