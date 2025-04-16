#  Reset USB Device

import subprocess

class usbReset():
    def __init__(self, device_id="05e3:0515", bus=None, dev=None): #a16f:0304 or 05e3:0515
        self.device_id = device_id
        self.bus = bus
        self.dev = dev

    def reset_usb_device(self):
        """Resets the USB device given its vendor:device ID."""
        print(f'Attempting to reset {self.device_id}')
        if not self.bus or self.dev:
            self.set_usb()
        else:
            try:
                device_path = f"/dev/bus/usb/{self.bus}/{self.dev}"
                subprocess.run(["sudo", "usbreset", device_path])
                print(f"USB device {self.device_id} reset successfully.")
                return True
            except Exception as e:
                print(f"Error resetting USB: {e}")
            return False
    
    def set_usb(self):
        try:
            # Find the device path
            result = subprocess.run(["lsusb"], capture_output=True, text=True)
            #print("lsusb:\n",str(result))
            for line in result.stdout.split("\n"):
                if self.device_id in line:
                    self.bus, self.dev = line.split()[1], line.split()[3][:-1]  # Extract Bus and Device number
                    device_path = f"/dev/bus/usb/{self.bus}/{self.dev}"
                    subprocess.run(["sudo", "usbreset", device_path])
                    print(f"USB device {self.device_id} reset successfully.")
                    return True
            print("Device not found.")
        except Exception as e:
            print(f"Error resetting USB: {e}")
        return False

reset_usb_device = usbReset()