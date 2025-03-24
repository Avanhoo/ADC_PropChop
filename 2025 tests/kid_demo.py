from codrone_edu.drone import *

drone = Drone()
drone.open()

while True:
    input("Kill drone? ")
    drone.land()
    
