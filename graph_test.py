from math import sqrt
from time import sleep, monotonic
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

tStart = 0
timenow = 0
current = [0,0,0]
dist_to_target = 0



def graph(x,y,z):
    global current, tStart
    gScale = 40
    screen.fill('grey')
    # TEXT
    img = font.render(f'Time: {timenow - tStart}', True, 'black')
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
while True:
    graph(4,1,3)
