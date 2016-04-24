import socket
import pygame
import time

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

s = socket.socket()
host = '10.0.0.5'  # My IP
port = 12348
s.bind((host, port))
i = 0

s.listen(5)
while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    while True:
         pygame.event.get()
         Xaxis = int(joystick.get_axis(3)*127)
         Xaxis += 127;
         c.send(bytes(str(Xaxis), 'UTF-8'))
         time.sleep(.1)
    c.close()
