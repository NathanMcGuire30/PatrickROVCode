#!/usr/bin/env python3
# Code to run on the RPi

from socket import *
import math


def clamp(value, minvalue, maxvalue):
    return (min(max(value, minvalue), maxvalue))


def run():
    computerSocket = socket()
    computerAddress = '172.16.0.2'  # ip laptop
    computerPort = 12346
    computerSocket.connect((computerAddress, computerPort))

    arduinoAddress = ('172.16.0.3', 5000)
    arduinoSocket = socket(AF_INET, SOCK_DGRAM)

    while True:
        # read bytes and turn them into a meaningful string
        inbytes = (computerSocket.recv(1024))
        text = str(inbytes)
        text = text.split("'")
        inValuesString = text[1]

        # breaks out values from joystick and converts to floats
        surge = float(inValuesString.split(",")[0])
        sway = float(inValuesString.split(",")[1])
        yaw = float(inValuesString.split(",")[2])
        heave = float(inValuesString.split(",")[3])
        brightness = float(inValuesString.split(",")[4])  # Light brightness
        camTilt = float(inValuesString.split(",")[5])  # Light brightness

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
        yaw *= -1  # Steering scaling value.  More negative = harder steering.  Max is -1, effective min is -0.1

        frontLeftPower += yaw
        frontRightPower -= yaw
        rearLeftPower -= yaw
        rearRightPower += yaw

        # Vertical code
        leftVerticalPower = int(heave)
        rightVerticalPower = int(heave)

        frontLeftPower = clamp(frontLeftPower, -255, 255)
        rearLeftPower = clamp(rearLeftPower, -255, 255)
        frontRightPower = clamp(frontRightPower, -255, 255)
        rearRightPower = clamp(rearRightPower, -255, 255)
        rightVerticalPower = clamp(rightVerticalPower, -255, 255)
        leftVerticalPower = clamp(leftVerticalPower, -255, 255)

        # frontRightPower =  0
        # frontLeftPower = 0
        # rearRightPower = 0
        # rearLeftPower = 0
        # leftVerticalPower = 0
        # rightVerticalPower = 0

        fullData = str(int(frontRightPower * -1)) + "," + str(int(rearRightPower)) + "," + str(
            int(frontLeftPower * -1)) + "," + str(int(rearLeftPower * -1)) + "," + str(leftVerticalPower) + "," + str(
            rightVerticalPower) + "," + str(int(brightness)) + "," + str(int(camTilt)) + ",;"

        print(fullData)

        arduinoSocket.sendto(bytes(fullData, 'UTF-8'), arduinoAddress)  # send command to arduino

        # wait for response from Arduino
        fromArduino = (arduinoSocket.recv(1024))

        # Split out message from arduino
        text = str(fromArduino)
        text = text.split('"')
        text = text[1].split("'")
        batteryVoltage = text[0]
        loopTime = text[1]

        # send stuff to computer
        computerSocket.send(bytes(str(batteryVoltage + "'" + loopTime), 'UTF-8'))


if __name__ == '__main__':
    run()
    # computerSocket.close()
    # arduinoSocket.close()
