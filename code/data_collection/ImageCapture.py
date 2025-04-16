# source imagecapture/bin/activte

import cv2
import serial
import time
import sys
import glob
from ResetUSB import reset_usb_device

def find_vid_devices2():
    """Find available video devices and return a list of their indices."""
    video_devices = glob.glob("/dev/video*")
    print("Video devices found: ", video_devices)
    return sorted(int(device.replace("/dev/video", "")) for device in video_devices), video_devices

def capture_image2(save_path, capture=None):
    """Tries different cameras until it successfully captures an image."""
    
    if not isinstance(capture, cv2.VideoCapture):
        camera_indices = find_vid_devices2()[0]
        if not camera_indices:
            print("Error: No available cameras found.")
            reset_usb_device.reset_usb_device()
            return False

        print('Camera indices: ', camera_indices)

        for index in camera_indices:
            print(f"Trying camera at /dev/video{index}...")
            cap = cv2.VideoCapture(index)

            if cap.isOpened():
                print(f"Using camera at /dev/video{index}")
                new_capture = True  # Track if we created a new instance
                break
            else:
                cap.release()

        else:
            print("Error: Could not open any camera.")
            reset_usb_device.reset_usb_device()
            return False
    else:
        cap = capture
        new_capture = False

    try:
        for attempt in range(5):  # Retry capturing the frame up to 5 times
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(save_path, frame)
                print(f"Image saved to {save_path}")
                return True
            else:
                print(f"Error: Failed to grab frame (attempt {attempt + 1}/5)")
                reset_usb_device.reset_usb_device()
                time.sleep(1)

        print("Error: Camera failed to capture image after multiple attempts.")
        return False

    finally:
        if new_capture:
            cap.release()
            cv2.destroyAllWindows()

def capture_imageV(save_path):
    