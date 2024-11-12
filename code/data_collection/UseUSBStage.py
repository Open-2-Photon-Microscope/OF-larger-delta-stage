# sudo usermod -aG dialout $USER
# sudo chmod 666 /dev/ttyUSB1 # this one
# pip install -r requirements.txt
# MAKE SURE TO KILL IPYTHON BEFORE TRYING TO RUN AGAIN

import os
import subprocess

def grant_usb_access(device_path):
    try:
        # Change the permissions of the device
        subprocess.run(['sudo', 'chmod', '666', device_path], check=True)
        print(f"Permissions changed for {device_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to change permissions for {device_path}: {e}")

# Usage
device_path = '/dev/ttyUSB0'
grant_usb_access(device_path)


import belay

device = belay.Device(device_path, baudrate=115200)

@device.setup
def setup():
    from cart_del import Stage
    stage = Stage(skip_init=True)    


@device.task
def move_to(target: list):
    stage.move_to(target)
    position = [stage.X_pos, stage.Y_pos, stage.Z_pos]
    return position

@device.task
def move_rel(vector: list):
    stage.move_rel(vector)
    position = [stage.X_pos, stage.Y_pos, stage.Z_pos]
    return position

@device.task
def use_controller():
    stage.use_controller()

@device.task
def live_move():
    stage.live_move()

@device.task
def zero():
    stage.zero()