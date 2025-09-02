from linuxpy.video.device import Device, V4L2Error
import glob


def capture_image2(filepath,opt=0):
    devices = sorted(glob.glob('/dev/video*'))
    # Open the camera device
    for dev in devices:
        try:
            g = int(dev.split('video')[1])
            with Device.from_id(g) as camera:
                frame = next(iter(camera))  # Capture a single frame
                frame.array.tofile(filepath)
                print(f"Frame saved as {filepath}")
            return
        except V4L2Error:
            print(f'{dev} is not a capture device, skipping...')
        except Exception as e:
            print(f'Error opening {dev}:{e}')
    raise RuntimeError('None of the available devices worked')

if __name__ == '__main__':
    import time
    img_folder = '/media/marcus1/large_chungus/data_collection/'
    for i in range(10):
        capture_image2(img_folder+str(i)+'.raw')
        time.sleep(0.1)
