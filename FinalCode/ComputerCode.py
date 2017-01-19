#Code to run on the computer

import socket
import pygame
import time

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()


host = '10.0.0.7'  # My IP.  Will need to be changed most times the code is run
port = 12345       # the port to use
# IF YOU STOP THE COMPUTER CODE BEFORE YOU STOP THE PI CODE,THE PORT WON'T CLOSE CORRETLY AND YOU WILL HAVE
#TO CHANGE THE PORT.

i = 0
endLoop = False

s = socket.socket()
s.bind((host, port))

while True:
    s.listen(5)
    c, addr = s.accept()
    print('Got connection from', addr)
    while (endLoop == False):
        pygame.event.get()

        #read values
        Xaxis = int(joystick.get_axis(1)*-256)
        if Xaxis == -255:
            Xaxis = -256

        Yaxis = int(joystick.get_axis(0)*-256)
        if Yaxis == -255:
            Yaxis = -256

        Zaxis = int(joystick.get_axis(2)*-256)
        if Zaxis == -255:
            Zaxis = -256

        Taxis = int(joystick.get_axis(3)*-256)
        if Taxis == -255:
            Taxis = -256

        final = str(Xaxis) + "," + str(Yaxis) + "," + str(Zaxis) + "," + str(Taxis)
        try:
            c.send(bytes(final, 'UTF-8'))
        except (ConnectionResetError, BrokenPipeError):
            print("connection terminated")
            endLoop = True
        time.sleep(.1)
c.close()
