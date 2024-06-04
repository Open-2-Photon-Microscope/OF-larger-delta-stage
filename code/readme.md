
<a name="readme-top"></a>

<h3 align="center">Testing the delta stage : long term drift and XY accuracy</h3>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
	<a href="#protocols-used">Protocols used</a>
	 <ul>
        <li><a href="#xy-translation-protocol">XY translation protocol</a></li>
        <li><a href="#long-term-drift-protocol">Long term drift protocol</a></li>
      </ul>
    <li>
      <a href="#code-usage">Code usage</a>
    </li>
      </ul>
    </li>
  </ol>
</details>



<!-- Protocols used -->
## Protocols used

Images were recorded on a 2 photon microscope (details?) using the large delta stage
(details?).

<!--  XY translation protocol-->
### XY translation protocol

We tested the delta stage movement accuracy in the X and Y axis by taking an initial picture 
near the centre of the specimen, then moving the stage across either axis or both axis simultaneously, 
before coming back to the theoretical zero location.

Aim : Translation error on small X AND / OR Y movements

Image sequence : start in (0;0) move on the X AND / OR Y axis, go back to (0;0)

Analysis : cross correlation
* Forward movement : When moving in X or Y, or XY, compare the input distance with the recorded displacement 
* Backward movement : When going back to 0 after a translation, is the original 0 matching ?

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Long term drift protocol-->
### Long term drift protocol

We tested the delta stage ability to maintain a stable location overtime near the centre of the stage and 
at locations further away in X AND/OR Y

Aim : Long term stability assessment

Image sequence : Choose a location (near centre or at X/Y extremes), 
take picture at different time (here 0, 30, 60 and 120 min)

Analysis : cross correlation
* Are the images at tx different from the original image at t0 ?

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Code usage

Important note on file naming : File names should contain the X Y and Z coordinates of the image, 
as well as a time when relevant. A numerical incrementing file ID is also necessary for image sorting. 
There is some flexibility such that ID_x_0_y_0_z_0 or ID_X00Y00Z00_t1 should both work, 
and small errors in ID numbering shouldn't affect the code (for e.g. ID duplication on consecutive files is ok, but not on distant files)

Scripts should be run as follow : 

1. Extract the coordinates of each raw image (from file name). This is done using the appropriate S1 script for each analysis :
* [S1_Get_table_of_coordinates_XY_analysis](S1_Get_table_of_coordinates_XY_analysis.py)
* [S1_Get_table_of_coordinates_long_term_drift](S1_Get_table_of_coordinates_long_term_drift.py)

This extracts the raw image path, image ID, X, Y and Z theoretical location and time when relevant.
For XY analysis, it also detects the nearest files at location (0;0;0), taken before and after the image of interest (relies on accurate ID numbering)
 (uses code/Function_1_Find_nearest_images_XY_analysis.py).
The parameter "slice_nbr = 200" should be adapted to match the number of slices recorded 
and is used to explude images that are erroneous (i.e. not enough slices).
It saves the data in a .csv coordinate table.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

2. Apply  Z projection and ehance images contrast on raw stack.tiff files with script S2:
* [S2_Z_projection_and_contrast_enhancement](S2_Z_projection_and_contrast_enhancement.py) (using [Function_2_Z_projection](Function_2_Z_projection.py))

From the previously created .csv coordinate table, reads each relevant image and averages all slices in the stack.
It outputs the projected images as .tiff with normalised and stretched intensity to increase contrast.
It also produces a new .csv table containing the same data as in 1- but with image path updated to the matching Z projected image.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

3. Compute a rigid transformation by phase cross correlation (i.e. without depth, only scale + translation + eventually rotation) using the appropriate S3 script :
* [S3_Align_with_skimage_cross_correlation_XY_analysis](S3_Align_with_skimage_cross_correlation_XY_analysis.py) (using [Function_3_Phase_cross_correlation_skimage_XY_analysis](Function_3_Phase_cross_correlation_skimage_XY_analysis.py))
* [S3_Align_with_skimage_cross_correlation_long_term_drift](S3_Align_with_skimage_cross_correlation_long_term_drift.py) (using [Function_3_Phase_cross_correlation_skimage_long_term_drift](Function_3_Phase_cross_correlation_skimage_long_term_drift.py))

For details on the cross correlation see https://scikit-image.org/docs/stable/auto_examples/registration/plot_register_translation.html

Outputs a summary image for each translation value or each time showing the result of the skimage transformation, the translations values and the theoretical values.
It also save all transformation values in a new .csv table.

Example of transformation after a translation in Y : 

![005_Registration_y0_x120_cross_corr](https://github.com/Open-2-Photon-Microscope/OF-larger-delta-stage/assets/83412687/b335a413-7616-4240-809f-57d132664fbb)

Example of transformation at a single point across 120 min :

![001_Y_positive_drift](https://github.com/Open-2-Photon-Microscope/OF-larger-delta-stage/assets/83412687/f5af734c-3b2a-4741-b056-f839e9fcdbbf)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

4. Create graphs of the results using the script S4 corresponding to the required analysis :
* [S4_Cross_correlation_graphs_XY_analysis](S4_Cross_correlation_graphs_XY_analysis.py)
* [S4_Cross_correlation_graphs_long_term_drift](S4_Cross_correlation_graphs_long_term_drift.py)

Examples of analysis for XY translation :
* Absolute error in both axis for single X or Y translations :
  
![Protocol_1_Error_in_each_group](https://github.com/Open-2-Photon-Microscope/OF-larger-delta-stage/assets/83412687/7a8926c2-c487-4e2d-b65d-5362eb3acd61)

* Theoretical translation vs recorded translation for X and Y translations :
  
![Protocol_2_Theoretical_vs_recorded_translation](https://github.com/Open-2-Photon-Microscope/OF-larger-delta-stage/assets/83412687/f7939ec2-631f-494d-a9fb-feaae46cf590)

* Error in X or Y after returning to the (0;0) location : 

![Protocol_1_Going_back_to_Zero_translation_error](https://github.com/Open-2-Photon-Microscope/OF-larger-delta-stage/assets/83412687/8fada742-8c01-4391-a916-a8fcf7927c4b)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
