# source imagecapture/bin/activte

import cv2
import serial
import time
import sys


def capture_image(save_path,capture=False):
    if type(capture) != cv2.VideoCapture:
        # Initialize the webcam
        cap = cv2.VideoCapture(0)
    else:
        cap = capture

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Cannot open the webcam")
        sys.exit()
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Failed to grab frame")
        sys.exit()
        return

    # Save the captured image to the specified path
    cv2.imwrite(save_path, frame)
    print(f"Image saved to {save_path}")

    if type(capture) != cv2.VideoCapture:
        # Release the webcam and close any OpenCV windows
        cap.release()
        cv2.destroyAllWindows()
