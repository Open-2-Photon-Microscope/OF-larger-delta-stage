# AUTOMATE DATA COLLECTION

import ImageCapture as img
import UseUSBStage as usb
import time
from numpy import linspace


class Collector():
    def __init__(self,
                 save_path='/home/marcus1/Documents/data_collection/drift_data/',
                 X_range=1000,
                 Y_range=1000):

        self.X_range: int = X_range
        self.Y_range: int = Y_range
        self.save_path: str = save_path
        self.device_path:str
        usb.setup()
    
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
                         start_ID=0):
        filename = ''
        save_path = ''
        i = 0
        if coord_list == []:
            coord_list = self.coords
        
        time.sleep(wait)

        #img.capture_image(self.save_path + f'{start_ID}_x0y0z0_start.jpg')
        #start_ID += 1
        for position in coord_list:
            i += 1
            pos = usb.move_to(position)
            time.sleep(rest)
            # NB filename values are /2 to illustrate um not steps
            filename = f"_x{round(pos[0]/2)}y{round(pos[1]/2)}z{round(pos[2]/2)}_t"
            save_path = self.save_path + filename # obsolete?
            mins = 0

            for t in range(len(time_delay)): # how many time frames
                for b in range(img_burst): # images per frame
                    mins += time_delay[t]
                    img.capture_image(self.save_path + str(start_ID) + filename + str(t) + f'_m{mins}.jpg')
                    start_ID += 1
                    time.sleep(rest)
                time.sleep(time_delay[t])
            # TODO: take multiple images for final image
            img.capture_image(self.save_path + str(start_ID) + filename + f'{len(time_delay)}.jpg')
            start_ID += 1
            print(f"{i} out of {len(coord_list)} complete")
        
        usb.move_to([0,0,0])
        # for b in range(img_burst): # images per frame
        #     time.sleep(rest)
        #     img.capture_image(self.save_path + f'{start_ID}' + f'_x0y0z0_t0.jpg')
        #     start_ID += 1
   

def set_times(delay_mins=10, times=12):
    time_delay_list = [0]
    for i in range(times):
        time_delay_list.append(delay_mins*60)
    print(time_delay_list)
    return time_delay_list

#time_delay_list = [60*60,60*60]
time_delay_list = set_times()

X_range = 9000
Y_range = 9000

if __name__ == "__main__":
    if input('Go? [y/n] ').lower() == 'y':
        c = Collector(X_range=X_range, Y_range=Y_range)
        c.gen_target_pos(3,3)
        c.automate_collect(time_delay=time_delay_list,rest=30, img_burst=1)
    
    elif input('Test? [y/n]').lower() == 'y':
        c = Collector(X_range=1, Y_range=1)
        c.gen_target_pos(1,1)
        c.automate_collect(time_delay=[1,1],rest=3, img_burst=1)
