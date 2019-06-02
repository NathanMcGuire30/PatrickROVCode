#!/usr/bin/env python3
#Code that tests the joystick math

import pygame
import time
import math

pygame.init()
pygame.joystick.init()

joystick0 = pygame.joystick.Joystick(0)
joystick0.init()

endloop = False

while endloop == False:
    pygame.event.get()

    #read values from joystick
    Xaxis = int(joystick0.get_axis(1) * -255)
    if Xaxis == -254:
        Xaxis = -255

    Yaxis = int(joystick0.get_axis(0) * -255)
    if Yaxis == -254:
    	Yaxis = -255

    if joystick0.get_button(2) == 1:
    	endloop = True

    surge = Xaxis
    sway = Yaxis

    #print(sway)

    angle = math.atan2(sway, surge)								 #convert to polar
    angle = angle/math.pi * 180                                  #convert to degrees
    #angle -= 135                                                 #rotate cordinates
    if angle < 0:                                                #get rid of negative angles
        angle += 360
    if surge == 0 and sway == 0:                                 #Fix values for when joystick is centered
        angle = 0.0

    #print(angle)

    absolutePower = math.sqrt(surge * surge + sway * sway)       #Some scaling to make it easier to control from a square profile joystick (needs work eventually)
    if absolutePower != 0:
        if abs(surge) > abs(sway):
          maxPowerScaleFactor = 255/surge
        else:
            maxPowerScaleFactor = 255/sway
        maxPower = absolutePower * maxPowerScaleFactor
        scaledPower = abs((absolutePower/maxPower)*255)
    else:
        scaledPower = 0

    
    if sway >=0 and surge >= 0:
    	frontRightPower = scaledPower
    	frontLeftPower = int(scaledPower * math.cos(math.radians(2*angle)))
    elif sway < 0 and surge >= 0:
    	frontRightPower = int(scaledPower * math.cos(math.radians(2*angle)))
    	frontLeftPower = scaledPower
    elif sway < 0 and surge < 0:
    	frontRightPower = -scaledPower
    	frontLeftPower = int(-scaledPower * math.cos(math.radians(2*angle)))
    elif sway >=0 and surge < 0:
    	frontRightPower = int(-scaledPower * math.cos(math.radians(2*angle)))
    	frontLeftPower = -scaledPower

    rearRightPower = -frontLeftPower
    rearLeftPower = -frontRightPower

    #print(angle)
    #print(frontLeftPower)
    #print(round(math.cos(math.radians(2*angle)), 3))
    print(str(int(frontRightPower)) + "," + str(int(rearRightPower)) + "," + str(int(frontLeftPower)) + "," + str(int(rearLeftPower)))