import serial
import time

ser = serial.Serial("/dev/ttyACM0", 9600, write_timeout=.1)
message = 1
while True:
    ser.write(str(message).encode())
    message+=1

    time.sleep(.5)