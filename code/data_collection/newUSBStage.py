import glob
from belay import Device

def find_usb_device(class_based=True):
    possible_ports = glob.glob("/dev/ttyUSB*")  # List all USB serial devices
    if not possible_ports:
        raise RuntimeError("No USB device found!")
    
    for port in possible_ports:
        try:
            print(f"Trying {port}...")
            if class_based == True:
                device = StageDevice(port,attempts=-1)
            else:
                device = Device(port,attempts=-1)
                device("from cart_del import Stage")
                device("stage = Stage(skip_init=True)")
            print(f"Connected to {port}")

            return device  # Return the first successful connection
        except Exception as e:
            print(f"Failed to connect to {port}: {e}")
    
    raise RuntimeError("Could not connect to any USB device")

class StageDevice(Device):
    @Device.setup(autoinit=True)
    def setup():
        from cart_del import Stage
        stage = Stage(skip_init=True)

    @Device.task
    def move_to(target: list):
        #stage.zero(skip=True)
        stage.move_to(target)
        position = [stage.X_pos, stage.Y_pos, stage.Z_pos]
        print(position)
        return position

    @Device.task
    def smooth_move():
        stage.smooth_move()

    @Device.task
    def zero():
        stage.zero(True)

    @Device.task
    def is_running():
        if stage.motorA.is_running or stage.motorB.is_running or stage.motorC.is_running:
            return True
        else:
            return False