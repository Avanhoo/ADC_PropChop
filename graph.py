from codrone_edu.drone import *
import numpy as np
from time import sleep, monotonic
from simple_pid import PID
from LiveGraph import LiveGraph


drone = Drone()
drone.pair()


drone.set_initial_pressure()
drone.set_drone_LED(255, 255, 255, 50)
pidThrottle = PID(60, 2, 0.1, setpoint=1, output_limits=(-100,100)) # throttle (up and down) pid
pidThrottle.time_fn = monotonic
pidThrottle.sample_time = 0.01

pidRoll = PID(60, 2, 0.1, setpoint=1, output_limits=(-100,100)) # throttle (up and down) pid
pidRoll.time_fn = monotonic
pidRoll.sample_time = 0.01

pidPitch = PID(60, 2, 0.1, setpoint=1, output_limits=(-100,100)) # throttle (up and down) pid
pidPitch.time_fn = monotonic
pidPitch.sample_time = 0.01



#print(drone.get_color_data()) # get color working

print("done1")
def move(x,y,z,v,h,r): #positionX, positionY, positionZ, velocity, heading, rotationalVelocity
    centering = True
    pidThrottle.setpoint = z
    #dist = np.sqrt(x^2 + y^2 + z^2)
    drone.send_absolute_position(x, y, z, v, h, r) # Tells drone to move
    while centering:
        current = drone.get_position_data()[1:]
        current = [ round(elem, 2) for elem in current ] #List of x, y z positions

        drone.set_pitch(-pidPitch(current[1]))
        drone.set_roll(-pidRoll(current[0]))
        drone.set_throttle(pidThrottle(current[2]))
        drone.move()

        print(current[2]) # Printing and graphing
        LG.update([[current[2],z-current[2]]])
        sleep(.01)


LG = LiveGraph(
    (
        (100, ["position", "error"], "graph1", ["g", "r", ]),
        # A graph with the name graph1 and two lines one red and one blue with 
        # the names line 1 and line 2
    ),
)

drone.takeoff()
move(0,0,0,1,0,0)
print("takeoff")
try: # Handles errors
    move(0,0,0,1,0,0)
    print("------moving on------")
except Exception as error: 
    print(error)
#drone.send_absolute_position(0,0,1,1,0,0)


drone.hover(1)
drone.land()
drone.close()

# code doesn't wait for drone to reach position, it continues immediately