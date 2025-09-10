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

def move_collect(positions, folder_path, backlash, i=0,rest=10):
    ''' Take picture at zero
    Iterate through each position:
        Move to position
        Take a picture there
        Move back to zero
        New picture
    '''
    save_path = folder_path + f'rep_data_backlash{backlash}_{datetime.today()}/'
    os.makedirs(save_path, exist_ok=True)

    for position in positions:
        #make new usb device
        stage = usb.find_usb_device(False)
        
        # initial image
        pos = [0,0,0]
        stage("stage.zero(True)")
        filepath = save_path + str(i).zfill(3) + f'_x{pos[0]}_y{pos[1]}_z{pos[2]}.raw'
        time.sleep(rest)
        img.capture_image2(filepath)
        i += 1

        #execute movement on device
        pos = position
        stage(f"stage.move_to({position})")
        time.sleep(rest)
        #capture image
        #names to follow the format nnn_x?_y?_z?.raw
        filepath = save_path + str(i).zfill(3) + f'_x{pos[0]}_y{pos[1]}_z{pos[2]}.raw'
        img.capture_image2(filepath)
        i+=1
    
        # return to zero + capture
        pos = [0,0,0]
        stage(f"stage.move_to([0,0,0])")
        filepath = save_path + str(i).zfill(3) + f'_x{pos[0]}_y{pos[1]}_z{pos[2]}.raw'
        time.sleep(rest)
        img.capture_image2(filepath)
        i+=1
        stage.close()
    return i


folder_path = '/media/marcus1/large_chungus/data_collection/'

#generate movement pattern
distances_um = [5,10,50,250,1000,4500]
#distances_um = [4500]
distances_steps = [i*2 for i in distances_um]
positions = generate_positions(distances_steps)

reps = 50

if __name__ == '__main__':
    start_time = int(time.time())
    for rep in range(reps):
        print(f'rep {rep} of {reps}')
        
        # start the device
        
        #stage("stage.zero(True)")
        move_collect(positions,folder_path,backlash=50,rest=10)
        #stage.close()
        end_time = int(time.time())
        time_taken = end_time-start_time
        print(f'That took {time_taken} seconds')