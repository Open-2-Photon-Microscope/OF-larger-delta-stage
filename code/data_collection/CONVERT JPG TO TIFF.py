# CONVERT JPG TO TIFF
 
import os
from skimage import io, util
from skimage.color import rgb2gray
import numpy as np
import cv2
from yuyv_to_rgb_cap import yuyv2rgb

def convert_jpg_to_tiff(folder_path,filetype_in='.jpg',filetype_out='.tiff',do_the_raw=False):
    # Ensure the folder path exists
    if not os.path.isdir(folder_path):
        print(f"Error: The folder {folder_path} does not exist.")
        return

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(filetype_in):
            # Create the full file path for the input JPG and output TIFF
            jpg_path = os.path.join(folder_path, file_name)
            tiff_path = os.path.join(folder_path, os.path.splitext(file_name)[0] + filetype_out)
            
            if do_the_raw == False:
                # Read the JPG image
                image = io.imread(jpg_path).astype(np.float32)
            if do_the_raw == True:
                image = yuyv2rgb(jpg_path, np.float32)
            image /= image.max()
            image = rgb2gray(image)
            image = util.img_as_uint(image) # convert to 16bit values
            
            # Save the image as TIFF
            io.imsave(tiff_path, image)
            print(f"Converted: {file_name} -> {os.path.basename(tiff_path)}")

# Usage
if __name__ == "__main__":
    folder_path = input("Enter the path to the folder: ")
    convert_jpg_to_tiff(folder_path,'.raw',do_the_raw=True)
