import pygame
import time
pygame.init()

pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

while True:
    pygame.event.get()
    print(joystick.get_button(2))
    time.sleep(.1)