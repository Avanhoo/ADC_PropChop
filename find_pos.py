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

drone.takeoff()
print("takeoff")
saved = []
pos_count = 1

while True:
  if input("Record?") == "exit":
    break
  else:
    current = drone.get_pos_x(unit="m"), drone.get_pos_y(unit="m"), round(drone.get_pos_z(unit="m"), 3)
    #saved.append(pos_count) # Saves step number
    saved.append(current[0]) # Saves position and 2 empty spaces for adjustments
    saved.append(current[1])
    saved.append(current[2])
    pos_count += 1
    print(saved)
  sleep(.1)

drone.land()
drone.close()
#python c:/Users/avanhoo2498/Documents/PropChop/find_pos.py

