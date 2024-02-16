from codrone_edu.drone import *
import numpy as np
from time import sleep, monotonic
from simple_pid import PID
from LiveGraph import LiveGraph
import traceback


drone = Drone()
drone.pair()


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
def move(x,y,z): #positionX, positionY, positionZ, heading, rotationalVelocity
    centering = True
    tolerance = .1 # How close the drone has to be to be to move on
    start_time = drone.get_position_data()[0]
    global Timeout
    pidPitch.setpoint = x
    pidRoll.setpoint = y
    pidThrottle.setpoint = z
    
    while centering: # Loops until it's in position
        current = drone.get_pos_x(unit="m"), drone.get_pos_y(unit="m"), round(drone.get_pos_z(unit="m"),3)# gets rounded List of x, y, z positions

        if abs(current[0]-x) <= tolerance and abs(current[1]-y) <= tolerance and abs(current[2]-z) <= tolerance: # Checks if drone is in correct position
            centering = False
            print(f"--- In position {x}, {y}, {z} ---")
            break
        elif drone.get_position_data()[0] - start_time >= Timeout: # Timeout for if drone can't center
            centering = False
            print(f"--- Centering Timeout ---")
            break

        
        drone.set_pitch(pidPitch(current[0])) # Please note pitch is x and roll is y
        drone.set_roll(-pidRoll(current[1])) # Roll is backwards in the library
        drone.set_throttle(pidThrottle(current[2]))
        drone.move(.1)

        print((current[0]-x) , (current[1]-y), (current[2]-z), -pidRoll(current[1])) # Printing and graphing
        LG.update([[current[2],z-current[2]]]) # Slows down code, only use for tuning
        sleep(.01)



LG = LiveGraph(
    (
        (100, ["x", "error"], "graph1", ["g", "r", ]),
        # A graph with the name graph1 and two lines one red and one blue with 
        # the names line 1 and line 2
    ),
)

drone.takeoff()
print("takeoff")

move(0,0,1) # Testing movements

move(1,.5,1)

move(0,0,1)

# try: # Handles errors
#     move(0,0,0,0,0)
#     print("------moving on------")
# except Exception as error: 
#     traceback.print(error)


drone.hover(1)
drone.land()
drone.close()

# code doesn't wait for drone to reach position, it continues immediately
