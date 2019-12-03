#!/usr/bin/env python3
# Code to run on the computer

import socket
import pygame
import time

pygame.init()
pygame.joystick.init()

joystick0 = pygame.joystick.Joystick(0)
joystick0.init()

host = '172.16.0.2'  # My IP.;p
port = 12346  # the port to use
# IF YOU STOP THE COMPUTER CODE BEFORE YOU STOP THE PI CODE,THE PORT WON'T CLOSE CORRECTLY AND YOU WILL HAVE
# TO CHANGE THE PORT.

toggle1 = 1
i = 0
endLoop = False

s = socket.socket()
s.bind((host, port))

camTiltDelta = 5
defaultCamTilt = 80

while True:
    brightness = 0
    camTilt = defaultCamTilt
    print("waiting for connection\nSafe to stop program")  # wait for connection
    endLoop = False
    s.listen(5)
    computerSocket, addr = s.accept()
    print('Got connection from', addr)
    print("Make sure to stop the program on the robot before the computer\n")

    while (endLoop == False):  # Loop once we get connection
        pygame.event.get()

        # read values from joystick
        Xaxis = int(joystick0.get_axis(1) * -255)
        if Xaxis == -254:
            Xaxis = -255

        Yaxis = int(joystick0.get_axis(0) * -255)
        if Yaxis == -254:
            Yaxis = -255

        Zaxis = int(joystick0.get_axis(2) * -255)
        if Zaxis == -254:
            Zaxis = -255

        Taxis = int(joystick0.get_axis(3) * -255)
        if Taxis == -254:
            Taxis = -255

        # Lights Controll
        brightnessScaleFactor = 10 ** (len(str(brightness)) - 1)
        if joystick0.get_button(2) == 1:  # Lights dimmer
            brightness -= brightnessScaleFactor
        elif joystick0.get_button(4) == 1:  # lights brighter
            brightness += brightnessScaleFactor

        if joystick0.get_button(0) == 1:
            if toggle1 == 1:
                brightness = 255
            else:
                brightness = 0
            toggle1 *= -1
            time.sleep(.2)

        if brightness > 255:
            brightness = 255
        elif brightness < 0:
            brightness = 0

        # Camera tilt control
        if joystick0.get_button(3) == 1:  # Cam down
            camTilt += camTiltDelta
        elif joystick0.get_button(5) == 1:  # Cam up
            camTilt -= camTiltDelta

        if joystick0.get_button(1) == 1:
            camTilt = defaultCamTilt

        if camTilt > 180:
            camTilt = 180
        elif camTilt < 0:
            camTilt = 0

        # Send data to rPI
        final = str(Xaxis) + "," + str(Yaxis) + "," + str(Zaxis) + "," + str(Taxis) + "," + str(brightness) + "," + str(
            camTilt)
        try:
            computerSocket.send(bytes(final, 'UTF-8'))
        except (ConnectionResetError, BrokenPipeError):
            print("closing connection")
            computerSocket.close()
            time.sleep(.5)  # pause to seem like the program is doing stuff
            endLoop = True

        # Receive data from rPI
        try:
            inbytes = computerSocket.recv(1024)

            inbytes = str(inbytes)
            text = inbytes.split('"')
            inValuesString = text[1].split("'")

            battVoltage = inValuesString[1]

            print(inValuesString)
        except(
        ConnectionResetError, BrokenPipeError, OSError, IndexError):  # if we no longer have comms, set values to zero
            inbytes = ("b'no return signal'")
            print("\n \n")

        time.sleep(.05)
