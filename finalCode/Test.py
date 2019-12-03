#!/usr/bin/env python3
# Code to run on the computer

from socket import *
import pygame
import time
import math

pygame.init()
pygame.joystick.init()

joystick0 = pygame.joystick.Joystick(0)
joystick0.init()

# IF YOU STOP THE COMPUTER CODE BEFORE YOU STOP THE PI CODE,THE PORT WON'T CLOSE CORRECTLY AND YOU WILL HAVE
# TO CHANGE THE PORT.

toggle1 = 1
i = 0
endLoop = False

arduinoAddress = ('172.16.0.3', 5000)
arduinoSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    brightness = 0
    print("waiting for connection\nSafe to stop program")  # wait for connection
    endLoop = False
    print("Make sure to stop the program on the robot before the computer\n")

    while (endLoop == False):  # send values
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

        surge = Xaxis
        sway = Yaxis
        heave = Taxis
        yaw = Zaxis

        # Strafe code
        angle = math.atan2(sway, surge)  # convert to polar
        angle = angle / math.pi * 180  # convert to degrees
        # angle -= 135                                                 #rotate coordinates
        if angle < 0:  # get rid of negative angles
            angle += 360
        if surge == 0 and sway == 0:  # Fix values for when joystick is centered
            angle = 0.0

        # print(angle)

        absolutePower = math.sqrt(
            surge * surge + sway * sway)  # Some scaling to make it easier to control from a square profile joystick (needs work eventually)
        if absolutePower != 0:
            if abs(surge) > abs(sway):
                maxPowerScaleFactor = 255 / surge
            else:
                maxPowerScaleFactor = 255 / sway
            maxPower = absolutePower * maxPowerScaleFactor
            scaledPower = abs((absolutePower / maxPower) * 255)
        else:
            scaledPower = 0

        if sway >= 0 and surge >= 0:
            frontRightPower = scaledPower
            frontLeftPower = int(scaledPower * math.cos(math.radians(2 * angle)))
        elif sway < 0 and surge >= 0:
            frontRightPower = int(scaledPower * math.cos(math.radians(2 * angle)))
            frontLeftPower = scaledPower
        elif sway < 0 and surge < 0:
            frontRightPower = -scaledPower
            frontLeftPower = int(-scaledPower * math.cos(math.radians(2 * angle)))
        elif sway >= 0 and surge < 0:
            frontRightPower = int(-scaledPower * math.cos(math.radians(2 * angle)))
            frontLeftPower = -scaledPower

        rearRightPower = -frontLeftPower
        rearLeftPower = -frontRightPower

        # Steering code
        yaw *= -.5  # Steering scaling value.  More negative = harder steering.  Max is -1, effective min is -0.1

        frontLeftPower += yaw
        frontRightPower -= yaw
        rearLeftPower += yaw
        rearRightPower -= yaw

        # Vertical code
        leftVerticalPower = int(heave)
        rightVerticalPower = int(heave)

        fullData = str(int(frontRightPower * -1)) + "," + str(int(rearRightPower)) + "," + str(
            int(frontLeftPower)) + "," + str(int(rearLeftPower * -1)) + "," + str(leftVerticalPower) + "," + str(
            rightVerticalPower) + "," + str(int(brightness)) + ",;"

        print(fullData)

        arduinoSocket.sendto(bytes(fullData, 'UTF-8'), arduinoAddress)  # send command to arduino

        fromArduino = (arduinoSocket.recv(1024))

        # Split out message from arduino
        text = str(fromArduino)
        text = text.split('"')
        text = text[1].split("'")

        print(text)

        time.sleep(.05)
