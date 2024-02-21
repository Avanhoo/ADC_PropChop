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
  current = drone.get_pos_x(unit="m"), drone.get_pos_y(unit="m"), round(
      drone.get_pos_z(unit="m"), 3)
  print(saved)
  if input("Record?") == "exit":
    break
  else:
    saved.append(pos_count)
    saved.append(current)
    pos_count += 1
  sleep(.1)

drone.land()
drone.close()
#python c:/Users/avanhoo2498/Documents/find_pos.py
