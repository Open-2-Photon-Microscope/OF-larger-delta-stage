from linuxpy.video.device import Device
import glob


def capture_image2(filepath):
    g = int(glob.glob('/dev/video*')[0].split('video')[1])
    # Open the camera device
    with Device.from_id(g) as camera:
        frame = next(iter(camera))  # Capture a single frame
        frame.array.tofile(filepath)
        print(f"Frame saved as {filepath}")


if __name__ == '__main__':
    import time
    img_folder = '/home/marcus1/Documents/data_collection/'
    for i in range(10):
        capture_image2(img_folder+str(i)+'.raw')
        time.sleep(0.1)
