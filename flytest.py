from codrone_edu.drone import *
import numpy as np
from time import sleep, monotonic
from simple_pid import PID

drone = Drone()
drone.pair()


drone.set_initial_pressure()
drone.set_drone_LED(255, 255, 255, 50)
pidH = PID(.5, 0.1, 0.075, setpoint=1) # drop pid
pidH.time_fn = monotonic
pidH.sample_time = 0.01

print(drone.get_color_data())

drone.takeoff()
print("takeoff")


print("done1")
def move(x,y,z,v,h,r):
    centering = True
    drone.send_absolute_position(x, y, z, v, h, r) #positionX, positionY, positionZ, velocity, heading, rotationalVelocity
    while centering:
        current = drone.get_position_data([1,2,3])
        if (current[0] - x < .25) and (current[1] - y < .25) and (current[2] - z < .25):
            print(f"X err: {(current[0] - x < .25)}, Y err: {(current[1] - y < .25)}, Z err: {(current[2] - z < .25)}")
    
print("loop done")

drone.hover(1)
drone.land()
drone.close()

# code doesn't wait for drone to reach position, it continues immediately
