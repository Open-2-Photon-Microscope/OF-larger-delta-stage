from linuxpy.video.device import Device, BufferType, VideoCapture
from PIL import Image
import cv2

with Device.from_id(0) as cam:
    for i, frame in enumerate(cam):
        print(f"frame #{i}: {len(frame)} bytes")
        if i > 9:
            break

def capture_image(save_path):
    with Device.from_id(0) as cam:
        for frame in cam:
            print(frame)
            cv2.imwrite(save_path,frame)
            return
        
capture_image('/home/marcus1/Documents/data_collection/test.tif')