from codrone_edu.drone import *
from math import sqrt
from time import sleep, monotonic
from simple_pid import PID
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

drone = Drone()
drone.open()

t = 0 # Variables that must be global for the graphing to work
yfinal = 1.98
current = [0,0,0]
dist_to_target = 0


drone.set_initial_pressure()
drone.set_drone_LED(255, 255, 255, 50)
sleep(1)
pidThrottle = PID(100, 1.5, 0.1, setpoint=1, output_limits=(-100,100)) # throttle (up and down) pid
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
    global current, dist_to_target
    centering = True
    start_time = drone.get_position_data()[0]
    current = round(drone.get_pos_x(unit="m"),3), drone.get_pos_y(unit="m"), round(drone.get_pos_z(unit="m"),3)
    x *= 0.3048 # Convert feet to meters
    y *= -0.3048 # negative to make +y right
    z *= 0.3048

    pidPitch.setpoint = x
    pidPitch.tunings =      (65, 6, 3)
    pidRoll.setpoint = y
    pidRoll.tunings =       (65, 6, 3)
    pidThrottle.setpoint = z
    if current[2] < z: # Different tunings for ascending and descending
        pidThrottle.tunings =   (100, 12, 0.01) # UP
    else:
        pidThrottle.tunings =   (80, 8, 1) # DOWN
    
    while centering: # Loops until it's in position
        current = round(drone.get_pos_x(unit="m"),3), drone.get_pos_y(unit="m"), round(drone.get_pos_z(unit="m"),3)# gets rounded List of x, y, z positions
        dist_to_target = sqrt((current[0]-x)**2 + (current[1]-y)**2 + (current[2]-z)**2) # Calculates 3d distance to target position
        if dist_to_target <= .25:
            pidPitch.tunings =      (100, 4, 0)
            pidRoll.tunings =       (100, 4, 0)
            pidThrottle.tunings =   (120, 1, .01) # NEEDS FIXED
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

        graph(x,y,z)
        print(round(current[0]-x,2) , round(current[1]-y,2), round((z-current[2]),2), round(roll, 3)) # Printing and graphing
        sleep(.01)


def graph(x,y,z):
    global current, tStart
    gScale = 40
    screen.fill('grey')
    # TEXT
    img = font.render(f'Time: {drone.get_position_data()[0] - tStart}', True, 'black')
    screen.blit(img, (20, 50))
    img = font.render(f'X: {current[0]}', True, 'black')
    screen.blit(img, (20, 80))
    img = font.render(f'Y: {current[1]}', True, 'black')
    screen.blit(img, (20, 100))
    img = font.render(f'Z: {current[2]}', True, 'black')
    screen.blit(img, (20, 120))
    img = font.render(f'Error: {dist_to_target}', True, 'red')
    screen.blit(img, (20, 150))

    # SHAPES
    pygame.draw.rect(screen, 'black', (280, 280, 40, 40), 2) # Starting location
    pygame.draw.rect(screen, 'red', (295- y*gScale, 295- x*gScale, 10, 10)) # Target
    pygame.draw.circle(screen, 'blue', (300- current[1]*gScale, 300- current[0]*gScale), 10, 2) # Drone

    pygame.draw.line(screen, 'black', (500, 500), (550, 500), 3) # Ground line
    pygame.draw.rect(screen, 'red', (520, 495-z*gScale, 10, 10)) # Target vertical
    pygame.draw.ellipse(screen, 'blue', (515, 495-current[2]*gScale, 20, 10), 2) # Drone vertical

    pygame.display.flip()


tStart = drone.get_position_data()[0]
drone.takeoff()
print("takeoff")

move(0, 1, 5, tolerance=.1)# prepared for yellow loop
move(0, 4, 5)# through yellow
move(0, 1, 5)# back
move(0, 6, 5)# through yellow

move(-0.5, 5, 4, tolerance=.1)# preapared for green
move(-2,   5, 4)# through green
move(-0.5, 5, 4)# back
move(-2,   5, 4)# through green

move(-5.5, 5, 3, tolerance=.1)# over box
print("LANDING")
drone.land()
drone.close()