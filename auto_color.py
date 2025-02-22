from codrone_edu.drone import *
from math import sqrt
from time import sleep, monotonic
from simple_pid import PID


drone = Drone()
drone.open()

t=0
yfinal = 1.98
saved = ['1, 2.474, 0, 1.55', 
         '2, 2.635, 1.98, 1.4'] # CHECK Y VALUE
#['1, 2.029, 0, 1.394', '2, 2.829, 0.2, 1.622', '3, 2.806, 1.474, 1.148']

drone.set_initial_pressure()
drone.set_drone_LED(255, 255, 255, 50)
sleep(.5)
pidThrottle = PID(100, 1, 0.1, setpoint=1, output_limits=(-100,100)) # throttle (up and down) pid
pidThrottle.time_fn = monotonic
pidThrottle.sample_time = 0.01

pidRoll = PID(80, .1, 0.03, setpoint=1, output_limits=(-100,100)) # roll (left and right) pid
pidRoll.time_fn = monotonic
pidRoll.sample_time = 0.01

pidPitch = PID(80, .1, 0.03, setpoint=1, output_limits=(-100,100)) # pitch (forward and back) pid
pidPitch.time_fn = monotonic
pidPitch.sample_time = 0.01


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
def move(x,y,z, timeout=4.5, tolerance=.15): #positionX, positionY, positionZ, timeout, positional tolerance
    centering = True
    start_time = drone.get_position_data()[0]
    pidPitch.setpoint = x
    pidPitch.tunings =      (80, .1, 0.03)
    pidRoll.setpoint = y
    pidRoll.tunings =       (80, .1, 0.03)
    pidThrottle.setpoint = z
    pidThrottle.tunings =   (80, 1, 0.1)
    
    while centering: # Loops until it's in position
        current = round(drone.get_pos_x(unit="m"),3), drone.get_pos_y(unit="m"), round(drone.get_pos_z(unit="m"),3)# gets rounded List of x, y, z positions
        dist_to_target = sqrt((current[0]-x)**2 + (current[1]-y)**2 + (current[2]-z)**2) # Calculates 3d distance to target position
        if dist_to_target <= .25:
            pidPitch.tunings =      (100, .01, 0)
            pidRoll.tunings =       (100, .01, 0)
            pidThrottle.tunings =   (120, .01, .01) # NEEDS FIXED
        if dist_to_target <= tolerance: # Checks if drone is in correct position
            centering = False
            print(f"--- In position {x}, {y}, {z} ---")
            break
        elif drone.get_position_data()[0] - start_time >= timeout: # timeout for if drone can't center
            centering = False
            print(f"--- Centering timeout ---")
            break

        pitch = pidPitch(current[0])# Please note pitch is x and roll is y
        roll = -pidRoll(current[1])# Roll is backwards in the library
        throttle = pidThrottle(current[2])

        drone.set_pitch(pitch) 
        drone.set_roll(roll) 
        drone.set_throttle(throttle)
        drone.move(.1) # CHANGE TIME?

        #print(round(current[0]-x,3), round(pitch,3))
        print(round(current[0]-x,2) , round(current[1]-y,2), round((z-current[2]),2), round(roll, 3)) # Printing and graphing
        sleep(.01)



drone.takeoff()
print("takeoff")


while t < 60:
    for i in range(len(saved)):
        step = saved[i].split(",") # Splits each step into move parameters
        step = [float(u) for u in step] # converts strings to floats except for 0th element

        print(f"Step: {step[0]}: {step[1]}, {step[2]}, {step[3]}")
        if len(step) == 5: # if there are timout instructions run them
            move(step[1], step[2], step[3], step[4])
        else:
            move(step[1], step[2], step[3])
    t += 60# CHANGE
    if t < 15:
        print("returning...")
        move(0, yfinal, 1.4,     2, .2) # Square movement back to 0,0,1
        move(0, 0, 1.4,     3, .2)
    
    
print("landing")
move(2.635, 1.419, .8,     2, .1)
drone.land()
#exit() #REMOVE LATER
hue_raw = drone.get_color_data()[1]
sleep(.1)
if 0 <= hue_raw < 60:
    drone.set_drone_LED(255,0,0,100)
    print("RED")
    drone.takeoff()
    move(-.7, 0, .5,   1.25, .2)

elif 60 <= hue_raw < 180:
    drone.set_drone_LED(0,255,0,100)
    print("GREEN")
    drone.takeoff()
    move(0, -.7, .5,   1.25, .2)

elif 180 <= hue_raw:
    drone.set_drone_LED(0,0,255,100)
    print("BLUE")
    drone.takeoff()
    move(.7, 0, .5,   1.25, .2)
drone.land()
drone.close()


#python c:/Users/avanhoo2498/Documents/PropChop/auto_color.py
