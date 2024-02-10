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

#print(drone.get_color_data()) # get color working

print("done1")
def move(x,y,z,v,h,r): #positionX, positionY, positionZ, velocity, heading, rotationalVelocity
    centering = True
    err = .1
    time = 0
    #dist = np.sqrt(x^2 + y^2 + z^2)
    drone.send_absolute_position(x, y, z, v, h, r) # Tells drone to move
    while centering:
        current = drone.get_position_data()[1:]
        current = [ round(elem, 2) for elem in current ]
        if (abs(current[0] - x) < err) and (abs(current[1] - y) < err) and (abs(current[2] - z+1) < err):
            print("Centered")
        
        drone.set_controller_LED(abs(current[2] - z)*10, 0, 0, 1)
        print(f"X err: {(current[0] - x)}, Y err: {(current[1] - y)}, Z err: {(current[2] - z+1)}")

        if time >= 2: # Prevents loop from running forever
            centering = False
        else:
            time+= .1
            sleep(.1) 
'''
drone.takeoff()
drone.send_absolute_position(0,0,0,.5,0,0)
while True:
    print(f"Z height: {drone.get_position_data()[3]}")
    drone.hover(.1)
'''
drone.takeoff()
print("takeoff")
try: # Handles errors
    move(0,0,0,1,0,0)
    print("------moving on------")
    move(1,0,1,1,0,0)
    print("------moving on------")
    move(0,0,0,1,0,45)
except Exception as error: 
    print(error)
#drone.send_absolute_position(0,0,1,1,0,0)


drone.hover(1)
drone.land()
drone.close()

# code doesn't wait for drone to reach position, it continues immediately
