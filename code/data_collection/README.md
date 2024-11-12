# Image Capture Protocol for XY Drift Analysis:

The files in this folder pertain to using a USB microscope with the [3-axis controller]() and [OF-larger delta stage](https://github.com/Open-2-Photon-Microscope/OF-larger-delta-stage)In the [`/code/`](https://github.com/Open-2-Photon-Microscope/OF-larger-delta-stage/tree/main/code) folder is a pipeline for analysing .tiff files that are derived from 2-photon microscopy files, however modified versions are named with the prefix 'jpeg' since the images they deal with (still tiff format) originate as jpeg files from the microscope. These files are the ones that will be used below but are dependent on other files in the folder. The protocol they use pertains only to X and Y drift.

## Collecting the Data  

The requires an up-to-date model of the 3-axis controller, and a way of holding the microscope above the sample (anything with distinct features so that movement can be measured).  

1. Download the files from this [folder](https://github.com/Open-2-Photon-Microscope/OF-larger-delta-stage/tree/main/code/data_collection)
2. Ensure the sample is visible from the camera (e.g. with cheese)
3. Ensure the stage is at `[0, 0, 0]` 
4. Running collect_data.py will prompt user to select the folder into which `/drift_data_x/` and all images will be saved (where x is the number of of the iteration)
	1. _NB: This is currently not true, I designed this to get the job done on my computer and it doesn't yet generalise so nicely_
5. The user is then prompted to input the number of iterations. 
	- Each iteration will take images at 9 positions (a 3x3 grid  from `[-4500,-4500]` to `[4500, 4500]`). Images will be taken at 10-minute intervals for two hours (for a total of 13 images including T0).
	- Each iteration creates its own folder
	- The number and length of the intervals the images are taken in may be modified to suit users needs'
	- Choosing many iterations allows autonomous data collection that may run for days

## When it ends  

Once the script is finished running, it will have created many folders. I recommend moving these folders to their own single folder with a clear label and date before running the script again, which would otherwise overwrite them.

## Troubleshooting  

Sometimes trouble happens: _c'est la vie_.  

- The most common error that might happen is:
	`[ WARN:0@3839.300] global cap_v4l.cpp:889 requestBuffers VIDEOIO(V4L2:/dev/video0): failed VIDIOC_REQBUFS: errno=19 (No such device)`
	- __Solution__: 
		1. Unplug and replug the usb microscope
		2. If the terminal is still active run `usb.moveto([0,0,0])` otherwise you will need to re-home the device manually
		3. All iterations / counting will start from 0 again so make sure to move or rename collected data so it is not overwritten

 - Sometimes an error will be in relation to the microcontroller.
	 - __Solution__: 
		 1. close all other programs that relate to the controller (including exit() from the script execution)
		 2. if that doesn't work, try unplugging the controller and turning off the power and plugging it back in (make sure to cross your fingers for good luck)

---
# Analysis Protocol:

#TODO: update this part of the protocol
