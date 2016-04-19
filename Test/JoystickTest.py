import pygame
import time
pygame.init()

pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

while True:
    pygame.event.get()
    axis = joystick.get_axis(0)
    print(int(axis*255))
    time.sleep(.1)