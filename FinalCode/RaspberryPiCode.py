from socket import *

computerSocket = socket()
computerAddress = '10.0.0.15' # ip laptop
computerPort = 12345
computerSocket.connect((computerAddress, computerPort))

arduinoAddress = ('10.0.0.243', 5000)
arduinoSocket = socket(AF_INET, SOCK_DGRAM)
arduinoSocket.settimeout(1) #only wait 1 second for a resonse


while True:
    #read bytes and turn them into a meaningful string
    inbytes = (computerSocket.recv(1024))
    text = str(inbytes)
    text = text.split("'")
    inValuesString = text[1]

    #sends out values from joystick
    surge = inValuesString.split(",")[0]                        #Front-Back
    sway = inValuesString.split(",")[1]                         #Left-right
    yaw = inValuesString.split(",")[2]                          #turning
    heave = inValuesString.split(",")[3]                        #Up-down

    fullData = surge + "," + sway + "," + heave + "," + yaw
    arduinoSocket.sendto(bytes(fullData, 'UTF-8'), arduinoAddress) #send command to arduino

    print(surge.encode())
computerSocket.close()
