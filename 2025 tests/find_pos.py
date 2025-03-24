from codrone_edu.drone import *
import numpy as np
from math import sqrt
from time import sleep, monotonic
from simple_pid import PID
import traceback


drone = Drone()
drone.open()


drone.set_initial_pressure()
drone.set_drone_LED(255, 255, 255, 50)
pidThrottle = PID(140, 6, 0.01, setpoint=1, output_limits=(-100,100)) # throttle (up and down) pid
pidThrottle.time_fn = monotonic
pidThrottle.sample_time = 0.1

pidRoll = PID(60, 4, 0.01, setpoint=1, output_limits=(-100,100)) # throttle (up and down) pid
pidRoll.time_fn = monotonic
pidRoll.sample_time = 0.1

pidPitch = PID(60, 4, 0.01, setpoint=1, output_limits=(-100,100)) # throttle (up and down) pid
pidPitch.time_fn = monotonic
pidPitch.sample_time = 0.1



# color_data = drone.get_color_data()
# color = drone.predict_colors(color_data)

print("done1")
def move(x,y,z, timeout=6, tolerance=.1): #positionX, positionY, positionZ, timeout, positional tolerance
    centering = True
    start_time = drone.get_position_data()[0]
    pidPitch.setpoint = x
    pidRoll.setpoint = y
    pidThrottle.setpoint = z
    
    while centering: # Loops until it's in position
        current = drone.get_pos_x(unit="m"), drone.get_pos_y(unit="m"), round(drone.get_pos_z(unit="m"),3)# gets rounded List of x, y, z positions
        dist_to_target = sqrt((current[0]-x)**2 + (current[1]-y)**2 + (current[2]-z)**2) # Calculates 3d distance to target position

        if dist_to_target <= tolerance: # Checks if drone is in correct position
            centering = False
            print(f"--- In position {x}, {y}, {z} ---")
            break
        elif drone.get_position_data()[0] - start_time >= timeout: # timeout for if drone can't center
            centering = False
            print(f"--- Centering timeout ---")
            break

        
        drone.set_pitch(pidPitch(current[0])) # Please note pitch is x and roll is y
        drone.set_roll(-pidRoll(current[1])) # Roll is backwards in the library
        drone.set_throttle(pidThrottle(current[2]))
        drone.move(.1)

        print((current[0]-x) , (current[1]-y), round((current[2]-z),3)) # Printing and graphing
        sleep(.01)


drone.takeoff()
print("takeoff")
saved = []
pos_count = 1

while True:
    #print(drone.get_button_data())
    if drone.r1_pressed():
        current = drone.get_pos_x(unit="m"), drone.get_pos_y(unit="m"), round(drone.get_pos_z(unit="m"),3)
        saved.append(f"{pos_count}, {current[0]}, {current[1]}, {current[2]}")
        print(saved)
        pos_count += 1
        while drone.r1_pressed():
            pass
    sleep(.1)

# try: # Handles errors
#     move(0,0,0,0,0)
#     print("------moving on------")
# except Exception as error: 
#     traceback.print(error)



drone.land()
drone.close()

#python c:/Users/avanhoo2498/Documents/PropChop/find_pos.py
