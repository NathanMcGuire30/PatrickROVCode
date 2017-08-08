#!/usr/bin/env python3
#Code to run on the computer

import socket
import pygame
import time

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()


host = '172.16.0.4'  # My IP.  Will need to be changed most times the code is run
port = 12345       # the port to use
# IF YOU STOP THE COMPUTER CODE BEFORE YOU STOP THE PI CODE,THE PORT WON'T CLOSE CORRETLY AND YOU WILL HAVE
#TO CHANGE THE PORT.

i = 0
endLoop = False

s = socket.socket()
s.bind((host, port))

#This is a comment
while True:
    print("waiting for connection")                 #wait for connection
    endLoop = False
    s.listen(5)
    c, addr = s.accept()
    print('Got connection from', addr)

    while (endLoop == False):                       #send values
        pygame.event.get()

        #read values
        Xaxis = int(joystick.get_axis(1)*-255)
        if Xaxis == -254:
            Xaxis = -255

        Yaxis = int(joystick.get_axis(0)*-255)
        if Yaxis == -254:
            Yaxis = -255

        Zaxis = int(joystick.get_axis(2)*-255)
        if Zaxis == -254:
            Zaxis = -255

        Taxis = int(joystick.get_axis(3)*-255)
        if Taxis == -254:
            Taxis = -255

        final = str(Xaxis) + "," + str(Yaxis) + "," + str(Zaxis) + "," + str(Taxis)
        try:
            c.send(bytes(final, 'UTF-8'))
        except (ConnectionResetError, BrokenPipeError):
            print("connection terminated")
            endLoop = True
        time.sleep(.1)
c.close()
