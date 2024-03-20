from codrone_edu.drone import *
import numpy as np
from math import sqrt
from time import sleep, monotonic
from simple_pid import PID
import traceback


drone = Drone()
#drone.pair()
drone.open()

drone.set_initial_pressure()
drone.set_drone_LED(255, 255, 255, 50)
print("ALIVE")

while True:
    hue_raw = drone.get_color_data()[1] # Senses color and checks what it is
    sleep(.25)
    if 0 <= hue_raw < 60:
        drone.set_drone_LED(255,0,0,100)
        print("RED")
    if 60 <= hue_raw < 180:
        drone.set_drone_LED(0,255,0,100)
        print("GREEN")
    if 180 <= hue_raw:
        drone.set_drone_LED(0,0,255,100)
        print("BLUE")

sleep(2)