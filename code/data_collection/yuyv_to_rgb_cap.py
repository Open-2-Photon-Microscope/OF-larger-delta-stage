import numpy as np
import cv2

def yuyv2rgb(file_path, data_type=np.uint8, display=False):    
    # Assuming width and height of the image
    width = 640
    height = 480
    byte_count = height*width*2
    element_size = np.dtype(data_type).itemsize
    element_count = byte_count // element_size

    # Read raw YUYV frame from v4l2
    with open(file_path, "rb") as f:
        raw_data = np.fromfile(f, dtype=np.uint8, count=byte_count)  # 2 bytes per pixel (YUYV format)
        print("Raw data size:", raw_data.size)
        print("Expected size:", height * width * 2)
        

        im = raw_data.reshape(height, width, 2)

    # Convert YUYV to NumPy array
    #yuyv = np.frombuffer(raw_data, dtype=np.uint8).reshape((height, width, 2))

    # Convert YUYV to BGR using OpenCV
    bgr_image = cv2.cvtColor(im, cv2.COLOR_YUV2BGR_YUYV)
    print('conversion finished')

    bgr_image = bgr_image.astype(data_type)
    if data_type == np.float32:
        bgr_image = bgr_image.astype(data_type) / 255.0

    if display == True:
        # Display image
        cv2.imshow("Converted Image", bgr_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return bgr_image

#img = yuyv2rgb('/home/marcus1/Documents/data_collection/raw_test/9.raw',np.float32)