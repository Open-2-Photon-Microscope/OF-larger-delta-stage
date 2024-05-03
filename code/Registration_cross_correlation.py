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

def cross_correlation_xy(translated_index, coord, px_size):
    before_index = translated_index - 1
    after_index = translated_index + 1
    print(before_index, translated_index, after_index)

    before_path = coord.Image_path.values[before_index]
    translation_path = coord.Image_path.values[translated_index]
    after_path = coord.Image_path.values[after_index]

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

    coord['Direction'] = np.where((coord['X_input_microm'] > 0) &
                                  (coord['Y_input_microm'] == 0) &
                                  (coord['Z_input_microm'] == 0), 'X_positive', float("NaN"))
    coord['Direction'] = np.where((coord['X_input_microm'] < 0) &
                                  (coord['Y_input_microm'] == 0) &
                                  (coord['Z_input_microm'] == 0), 'X_negative', coord['Direction'])
    coord['Direction'] = np.where((coord['X_input_microm'] == 0) &
                                  (coord['Y_input_microm'] > 0) &
                                  (coord['Z_input_microm'] == 0), 'Y_positive', coord['Direction'])
    coord['Direction'] = np.where((coord['X_input_microm'] == 0) &
                                  (coord['Y_input_microm'] < 0) &
                                  (coord['Z_input_microm'] == 0), 'Y_negative', coord['Direction'])
    coord['Direction'] = np.where((coord['X_input_microm'] == 0) &
                                  (coord['Y_input_microm'] == 0) &
                                  (coord['Z_input_microm'] > 0), 'Z_positive', coord['Direction'])
    coord['Direction'] = np.where((coord['X_input_microm'] == 0) &
                                  (coord['Y_input_microm'] == 0) &
                                  (coord['Z_input_microm'] < 0), 'Z_negative', coord['Direction'])
    coord['Direction'] = np.where((coord['X_input_microm'] == 0) &
                                  (coord['Y_input_microm'] == 0) &
                                  (coord['Z_input_microm'] == 0), 'Zero', coord['Direction'])

    coord['theoretical_distance'] = (coord['X_input_microm']
                                     + coord['Y_input_microm']
                                     + coord['Z_input_microm'])
    coord = coord.astype({'theoretical_distance': 'float'})

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
