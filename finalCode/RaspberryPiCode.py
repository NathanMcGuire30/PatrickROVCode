#!/usr/bin/env python3
#Code to run on the RPi

from socket import *
import math

computerSocket = socket()
computerAddress = '172.16.0.2' # ip laptop
computerPort = 12346
computerSocket.connect((computerAddress, computerPort))

arduinoAddress = ('172.16.0.3', 5000)
arduinoSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    #read bytes and turn them into a meaningful string
    inbytes = (computerSocket.recv(1024))
    text = str(inbytes)
    text = text.split("'")
    inValuesString = text[1]

    #breaks out values from joystick and converts to floats
    surge = float(inValuesString.split(",")[0])                       #Front-Back
    sway = float(inValuesString.split(",")[1])                        #Left-right
    yaw = float(inValuesString.split(",")[2])                         #turning
    heave = float(inValuesString.split(",")[3])                       #Up-down
    brightness = float(inValuesString.split(",")[4])                  #Light brightness

    #Strafe code
    angle = math.atan2(surge, sway)
    angle = angle/math.pi * 180                                  #convert to degrees
    angle -= 135                                                 #rotate cordinates
    if angle < 0:                                                #get rid of negative angles
        angle += 360
    if surge == 0 and sway == 0:                                 #Fix values for when joystick is centered
        angle = 0.0

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

    frontLeftPower = int(scaledPower * math.cos(math.radians(angle)))
    frontRightPower = int(scaledPower * math.sin(math.radians(angle)))
    rearLeftPower = frontRightPower * -1
    rearRightPower = frontLeftPower * -1

    #INVERT
    frontRightPower *= -1
    rearRightPower *= -1

    #Steering code
    yaw *= -.5                       #Steering scaling value.  More negative = harder steering.  Max is -1, effective min is -0.1

    frontLeftPower += yaw
    frontRightPower -= yaw
    rearLeftPower += yaw
    rearRightPower -= yaw
    
    #Vertical code
    leftVerticalPower = int(heave)
    rightVerticalPower = int(heave)

    fullData = str(int(frontRightPower)) + "," + str(int(rearRightPower)) + "," + str(int(frontLeftPower)) + "," + str(int(rearLeftPower)) + "," + str(leftVerticalPower) + "," + str(rightVerticalPower) + "," + str(int(brightness)) + ",;"

    print(fullData)

    arduinoSocket.sendto(bytes(fullData, 'UTF-8'), arduinoAddress) #send command to arduino

    #wait for response from arduino
    fromArduino = (arduinoSocket.recv(1024))

    #Split out message from arduino
    text = str(fromArduino)
    text = text.split("'")
    inValuesString = text[1]

    #send stuff to computer
    computerSocket.send(bytes(str(inValuesString), 'UTF-8'))
computerSocket.close()
arduinoSocket.close()