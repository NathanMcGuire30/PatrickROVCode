import socket
import serial

s = socket.socket()
host = '10.0.0.7' # ip laptop
port = 12345
s.connect((host, port))

ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    #read bytes and turn them into a meaningful string
    inbytes = (s.recv(1024))
    text = str(inbytes)
    text = text.split("'")
    inValuesString = text[1]

    #sends out values from joystick
    surge = inValuesString.split(",")[0]                        #Front-Back
    sway = inValuesString.split(",")[1]                         #Left-right
    heave = inValuesString.split(",")[3]                        #Up-down
    ser.write(surge.encode())
    print(surge.encode())
s.close()
