# imagecapture/bin/activte

import cv2
import serial
import time

def capture_image(save_path):
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Cannot open the webcam")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Failed to grab frame")
        return

    # Save the captured image to the specified path
    cv2.imwrite(save_path, frame)
    print(f"Image saved to {save_path}")

    # Release the webcam and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    # Specify the path where the image will be saved
    save_path = '/home/marcus1/Documents/PhD/image1.jpg'
    capture_image(save_path)
