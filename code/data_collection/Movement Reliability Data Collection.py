# Automatic movement reliability data collection

import v4l_cap as img
import newUSBStage as usb
import time
import os
import gc
from numpy import linspace
from datetime import datetime
from ResetUSB import reset_usb_device

def generate_positions(distances,reps=1):
    positions = []
    for distance in distances:
        for x in range(-1,2):
            for y in range(-1,2):
                for r in range(reps):
                    positions.append([x*distance,y*distance,0])
    return positions

def move_collect(positions, folder_path, backlash, i=0):
    ''' Take picture at zero
    Iterate through each position
    Take a picture there.
    Move back to zero
    New picture
    '''
    for position in positions:
        reset_usb_device.reset_usb_device()
        # initial image
        pos = [0,0,0]
        filepath = folder_path + (f'rep_data_backlash{backlash}_{datetime.today()}/' + 
                            str(i).zfill(3) +
                            f'_x{pos[0]}_y{pos[1]}_z{pos[2]}.raw')
        img.capture_image2(filepath)
        
        #execute movement on device
        pos = stage.move_to(position)
        while stage.is_running == True:
            time.sleep(1)
        #capture image
        #names to follow the format nnn_x?_y?_z?.raw
        i += 1
        filepath = folder_path + (str(i).zfill(3) +
            f'_x{pos[0]}_y{pos[1]}_z{pos[2]}.raw')
        img.capture_image2(filepath)
        
        # return to zero + capture
        i += 1
        pos = stage.move_to([0,0,0])
        filepath = folder_path + (str(i).zfill(3) +
            f'_x{pos[0]}_y{pos[1]}_z{pos[2]}.raw')
        img.capture_image2(filepath)


folder_path = '/media/marcus1/large_chungus/data_collection/'

#generate movement pattern
distances_um = [5,10,50,100,250]
distances_steps = [i*2 for i in distances_um]
positions = generate_positions(distances_steps)

if __name__ == '__main__':
    start_time = int(time.time())
    # start the device
    stage = usb.find_usb_device()
    stage.zero()
    move_collect(positions,folder_path,backlash=50)
    stage.close()
    end_time = int(time.time())
    time_taken = end_time-start_time
    print(f'That took {time_taken} seconds')