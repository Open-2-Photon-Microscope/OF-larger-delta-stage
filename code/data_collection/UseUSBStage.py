# sudo usermod -aG dialout $USER
# sudo chmod 666 /dev/ttyUSB1 # this one
# pip install -r requirements.txt
# MAKE SURE TO KILL IPYTHON BEFORE TRYING TO RUN AGAIN

import glob
import time
import os
import subprocess
import belay

def find_usb_device():
    possible_ports = glob.glob("/dev/ttyUSB*")  # List all USB serial devices
    if not possible_ports:
        raise RuntimeError("No USB device found!")
    
    for port in possible_ports:
        try:
            print(f"Trying {port}...")
            device = belay.Device(port, baudrate=115200, attempts=-1)
            print(f"Connected to {port}")
            return device  # Return the first successful connection
        except Exception as e:
            print(f"Failed to connect to {port}: {e}")
    
    raise RuntimeError("Could not connect to any USB device")

def grant_usb_access(device_path):
    try:
        # Change the permissions of the device
        subprocess.run(['sudo', 'chmod', '666', device_path], check=True)
        print(f"Permissions changed for {device_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to change permissions for {device_path}: {e}")

# Usage
#device_path = '/dev/ttyUSB0'
#grant_usb_access(device_path)

#device = belay.Device(device_path, baudrate=115200)

device = find_usb_device()

@device.setup
def setup():
    from cart_del import Stage
    stage = Stage(skip_init=True) 
    
@device.task
def move_to(target: list):
    #stage.zero(skip=True)
    stage.move_to(target)
    position = [stage.X_pos, stage.Y_pos, stage.Z_pos]
    print(position)
    return position

@device.task
def move_rel(vector: list):
    stage.move_rel(vector)
    position = [stage.X_pos, stage.Y_pos, stage.Z_pos]
    return position

@device.task
def smooth_move():
    stage.smooth_move()

@device.task
def zero():
    stage.zero(True)

@device.task
def is_running():
    if stage.motorA.is_running or stage.motorB.is_running or stage.motorC.is_running:
        return True
    else:
        return False