from socket import *
import math

#test comment

computerSocket = socket()
computerAddress = '172.16.0.4' # ip laptop
computerPort = 12345
computerSocket.connect((computerAddress, computerPort))

arduinoAddress = ('172.16.0.3', 5000)
arduinoSocket = socket(AF_INET, SOCK_DGRAM)
arduinoSocket.settimeout(1) #only wait 1 second for a resonse

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

    #Strafe code
    angle = math.atan2(surge, sway)
    angle = angle/math.pi * 180                                  #convert to degrees
    angle -= 135                                                 #rotate cordinates
    if angle < 0:                                                #get rid of negative angles
        angle += 360
    if surge == 0 and sway == 0:                                 #Fix values for when joystick is centered
        angle = 0.0

    absolutePower = math.sqrt(surge * surge + sway * sway)
    if surge > sway:
        maxPowerScaleFactor = 255/surge
    else:
        maxPowerScaleFactor = 255/sway
    maxPower = absolutePower * maxPowerScaleFactor
    scaledPower = (absolutePower/maxPower)*255

    frontLeftPower = int(scaledPower * math.cos(math.radians(angle)))
    rearRightPower = int(scaledPower * math.sin(math.radians(angle)))
    rearLeftPower = frontLeftPower * -1
    frontRightPower = rearRightPower * -1

    print(scaledPower)
    #Steering code
    yaw *= .1                       #Steering scaling value.  Bigger = harder steering

    frontLeftPower += yaw
    frontRightPower -= yaw
    rearLeftPower -= yaw
    rearRightPower += yaw

    #Vertical code
    leftVerticalPower = heave
    rightVerticalPower = heave

    #fullData = frontLeftPower + "," + frontRightPower + "," + rearLeftPower + "," + rearRightPower + "," + leftVerticalPower + "," + rightVerticalPower

    #arduinoSocket.sendto(bytes(fullData, 'UTF-8'), arduinoAddress) #send command to arduino
computerSocket.close()
