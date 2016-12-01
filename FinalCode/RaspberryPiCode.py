import socket
import serial

s = socket.socket()
host = '10.0.0.7' # ip laptop
port = 12345
s.connect((host, port))

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=None)

while True:
    #read bytes and turn them into a meaningful string
    inbytes = (s.recv(1024))
    text = str(inbytes)
    text = text.split("'")
    inValuesString = text[1]

    #sends out values from joystick
    value = inValuesString.split(",")[0]
    ser.write(value.encode())
s.close()
