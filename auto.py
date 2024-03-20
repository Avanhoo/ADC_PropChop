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
sleep(.5)
pidThrottle = PID(140, 5, 0.01, setpoint=1, output_limits=(-100,100)) # throttle (up and down) pid
pidThrottle.time_fn = monotonic
pidThrottle.sample_time = 0.1

pidRoll = PID(60, 5, 0.02, setpoint=1, output_limits=(-100,100)) # throttle (up and down) pid
pidRoll.time_fn = monotonic
pidRoll.sample_time = 0.1

pidPitch = PID(60, 5, 0.02, setpoint=1, output_limits=(-100,100)) # throttle (up and down) pid
pidPitch.time_fn = monotonic
pidPitch.sample_time = 0.1

#[0, 0, 0.892, -0.046, -0.049, 0.892, -0.046, -0.049, 0.892, 0.924, -0.09, 1.409, 2.285, 0.024, 1.284, 2.285, -0.014, 1.439, 2.504, 0.86, 1.368, 2.513, 0.804, 0.65, 2.513, 1.4, .65]
saved = [1.226, 0, 1.303,    1.225, 0, 1.5,    2, 0, 1.5,    2.1, 0.638, 1.557,    2.1, 1.5, .65]
#           Through arch       Up to yellow    Through Yellow   Up to green     To pad

#saved = [1.226, 0, 1.303,    1.225, 0, 1.5,    1.7, 0, 1.5,      1.7, 0, 2.25, 1.225, 0, 2.25,     1.225, 0, 1.5,    2, 0, 1.5,      2, 0.638, 1.557,   2,1,1.557,       2,1,2.15,  2,0.638,2.15,       2, 0.638, 1.557,      2, 1.65, .65]
#RISKY       Through arch       Up to yellow    Through Yellow              LOOP                   Down to yellow     Through Y     To green          Through green          LOOP                    Down to green         To pad

print(len(saved))

for u in range(10):
    hue_raw = drone.get_color_data()[1] # Senses color and checks what it is
    sleep(.1)
    if 0 <= hue_raw < 60:
        drone.set_drone_LED(255,0,0,100)
        print("RED")
    if 60 <= hue_raw < 180:
        drone.set_drone_LED(0,255,0,100)
        print("GREEN")
    if 180 <= hue_raw:
        drone.set_drone_LED(0,0,255,100)
        print("BLUE")

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


drone.land()

for u in range(10):
    hue_raw = drone.get_color_data()[1] # Senses color and checks what it is
    sleep(.25)
    if 0 <= hue_raw < 60:
        drone.set_drone_LED(255,0,0,100)
        print("RED")
        drone.takeoff()
        move(1.4, 1.65, .5)
        drone.land()
    
    if 60 <= hue_raw < 180:
        drone.set_drone_LED(0,255,0,100)
        print("GREEN")
        drone.set_drone_LED(255,0,0,100)
        drone.takeoff()
        move(2, 1.05, .5)
        drone.land()

    if 180 <= hue_raw:
        drone.set_drone_LED(0,0,255,100)
        print("BLUE")
        drone.set_drone_LED(255,0,0,100)
        drone.takeoff()
        move(2.6, 1.65, .5)
        drone.land()

drone.close()

#python c:/Users/avanhoo2498/Documents/PropChop/auto.py
# move(1.3,0,1.3) # Up to yellow
# move(2.5,0,1.3) # Through yellow
# move(2.5,0, 1.5) # Up to green
# move(2.5,0.2, 1.5) # Through green
# move(2.5,1.4, 1) # Over landing pad
