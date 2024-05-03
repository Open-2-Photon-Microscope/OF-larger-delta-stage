Files should be used as follow : 
- 1. Run  Z_projection_and_contrast_enhancement.py on raw stack.tiff files (calls functions defined in Z_proj_functions.py). This script averages all slices in the stack, and outputs the projected images as .tiff with normalised and stretched intensity to increase contrast, and a .csv table containing each image, path, name, ID, and theoretical displacement values.
This step strongly relies on correct file naming (ID_x_value_y_value_z_value) and file order, and could be modified to allow for user error.

- 2. Run Sort_and_align_skimage_cross_correlation.py on the projected files obtained from 1. (calls functions defined in Registration_cross_correlation.py). This script applies a cross correlation function to align the images, and outputs a summary image for each set of 3 images (initial (0;0), translation (tx,ty), and return to (0;0)) depicting the aligned images, and the estimated displacement compared to the initial (0;0) in µm and pixels. It also saves a .csv table of these values.

![014_Registration_y0_x-120_cross_corr](https://github.com/Open-2-Photon-Microscope/OF-larger-delta-stage/assets/83412687/01e8ba4e-bc53-418b-a9e7-33a321def878)

- 3. Run Cross_correlation_graphs.py to obtain summary plots showing the error in X and Y translation, as well as the error in returning to zero after a known translation.
![X_translation_error](https://github.com/Open-2-Photon-Microscope/OF-larger-delta-stage/assets/83412687/4ca48ade-e93e-4aae-a60b-1be0851f8114)
![Y_translation_error](https://github.com/Open-2-Photon-Microscope/OF-larger-delta-stage/assets/83412687/f3ec1787-578b-4929-8c1d-76812a6ad58d)
![Zero_translation_error](https://github.com/Open-2-Photon-Microscope/OF-larger-delta-stage/assets/83412687/04c72859-14bb-4502-8233-af8642097ce0)

