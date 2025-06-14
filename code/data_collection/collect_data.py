# AUTOMATE DATA COLLECTION
# source imagecapture/bin/activte

import v4l_cap as img
import newUSBStage as usb
import time
import os
import gc
from numpy import linspace
from datetime import datetime
from ResetUSB import reset_usb_device

gc.collect()

class Collector():
    def __init__(self,
                 save_path='/media/marcus1/large_chungus/data_collection/drift_data_',
                 X_range=1000,
                 Y_range=1000,
                 ):

        self.X_range: int = X_range
        self.Y_range: int = Y_range
        self.save_path: str = save_path
        self.device_path:str

    
    def gen_target_pos(self, x_steps, y_steps):
        x_coords: list
        y_coords: list
        tot_coords: list

        if x_steps < 2:
            x_steps = 2
        if y_steps < 2:
            y_steps = 2

        x_coords = linspace(-self.X_range, self.X_range, x_steps).tolist()
        y_coords = linspace(-self.Y_range, self.Y_range, y_steps).tolist()

        tot_coords = [[int(x), int(y), 0] for x in x_coords for y in y_coords]
        self.coords = tot_coords


    def automate_collect(self, 
                         time_delay=[3],
                         coord_list=[],
                         img_burst=1,
                         rest=10, # rest while moving / between imgs
                         wait=0, # wait before starting
                         start_ID=0,
                         iter=0,
                         custom_path_text=''):
        save_path = self.save_path + str(iter) + str(datetime.today()) + custom_path_text+'/'
        os.makedirs(save_path, exist_ok=True)

        filename = ''
        i = 0
        if coord_list == []:
            coord_list = self.coords
        
        time.sleep(wait)

        for position in coord_list:
            i += 1
            q=0

            #create new usb device
            stage = usb.find_usb_device()
            stage.zero()
            pos = stage.move_to(position)
            stage.close() # avoid long connections

            for j in range(rest):
                print(q, end='\r')
                time.sleep(1)
                q+=1
            # NB filename values are /2 to illustrate um because the stage's internal measures are in STEPS
            filename = f"_x{round(pos[0]/2)}y{round(pos[1]/2)}z{round(pos[2]/2)}_t"
            mins = 0

            for t in range(len(time_delay)): # how many time frames
                for b in range(img_burst): # images per frame
                    mins += time_delay[t] #TODO move to after img.capture_image
                    img.capture_image2(save_path + str(start_ID) + filename + str(t) + f'_m{int(mins/60)}.raw',opt=1)
                    start_ID += 1
                    time.sleep(rest)
                time.sleep(time_delay[t])
            #img.capture_image(save_path + str(start_ID) + filename + f'{len(time_delay)}_m{mins + time_delay[-1]}.jpg')
            #start_ID += 1
            print(f"{i} out of {len(coord_list)} complete")
        
        stage = usb.find_usb_device()
        stage.zero()
        stage.close()
   

def set_times(delay_mins=10, times=12):
    time_delay_list = [0]
    for i in range(times):
        time_delay_list.append(delay_mins*60)
    print(time_delay_list)
    return time_delay_list

#time_delay_list = [60*60,60*60]
#time_delay_list = set_times()
time_delay_list = set_times(delay_mins = 1, times=10)

X_range = 9000
Y_range = 9000

if __name__ == "__main__":
    if input('Go? [y/n] ').lower() == 'y':
        c = Collector(X_range=X_range, Y_range=Y_range)
        c.gen_target_pos(3,3)
        iterations = int(input(f'Number of iterations? \nNB: each takes around {round(sum(time_delay_list)*9/3600,1)} hours. '))
        for i in range(iterations):
            print(f'Iteration {i}')
            reset_usb_device.reset_usb_device()
            c.automate_collect(time_delay=time_delay_list,rest=30, img_burst=1, iter=i,custom_path_text='20x1min')
        #c.cap.release()

    elif input('Test? [y/n]').lower() == 'y':
        c = Collector(X_range=900, Y_range=900)
        c.gen_target_pos(1,1)
        for i in range(3):
            print(f'run {i}')
            c.automate_collect(time_delay=[0,1,1,1,1,1,1,1,1],rest=10, img_burst=1, iter=i)
        #c.cap.release()