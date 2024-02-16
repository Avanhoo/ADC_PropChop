from codrone_edu.drone import *
import numpy as np
from time import sleep, monotonic
from simple_pid import PID
from LiveGraph import LiveGraph
import traceback


drone = Drone()
drone.pair()

drone.takeoff()
print("takeoff")

drone.set_pitch(100)
for i in range(200):
    drone.move()
    print(drone.get_position_data())
    print(drone.get_pos_x(unit="m"))
    sleep(.01)


drone.land()
drone.close()