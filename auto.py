from codrone_edu.drone import *
import numpy as np
from math import sqrt
from time import sleep, monotonic
from simple_pid import PID
import traceback


drone = Drone()
drone.pair()


drone.set_initial_pressure()
drone.set_drone_LED(255, 255, 255, 50)
pidThrottle = PID(140, 5, 0.01, setpoint=1, output_limits=(-100,100)) # throttle (up and down) pid
pidThrottle.time_fn = monotonic
pidThrottle.sample_time = 0.1

pidRoll = PID(60, 5, 0.01, setpoint=1, output_limits=(-100,100)) # throttle (up and down) pid
pidRoll.time_fn = monotonic
pidRoll.sample_time = 0.1

pidPitch = PID(60, 5, 0.01, setpoint=1, output_limits=(-100,100)) # throttle (up and down) pid
pidPitch.time_fn = monotonic
pidPitch.sample_time = 0.1

#[0, 0, 0.892, -0.046, -0.049, 0.892, -0.046, -0.049, 0.892, 0.924, -0.09, 1.409, 2.285, 0.024, 1.284, 2.285, -0.014, 1.439, 2.504, 0.86, 1.368, 2.513, 0.804, 0.65, 2.513, 1.4, .65]
saved = [1.226, -0.16, 1.303, 1.225, -0.162, 1.47, 2.717, 0.638, 1.557, 2.631, 0.638, 1.557]
print(len(saved))
# color_data = drone.get_color_data()
# color = drone.predict_colors(color_data)

print("done1")
def move(x,y,z, timeout=4, tolerance=.1): #positionX, positionY, positionZ, timeout, positional tolerance
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

for i in range(int(len(saved)/3)):
    print(f"Step {i}")
    
    move(saved[3*i], saved[3*i+1], saved[3*i+2])

# move(0,1,1.5)
# move(0,2,1.5)
# move(0,2,2)



drone.land()
drone.close()

#python c:/Users/avanhoo2498/Documents/PropChop/auto.py
