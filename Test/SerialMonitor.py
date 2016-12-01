import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
while True:
    s = str(ser.readline())
    s=s.split("'")
    t=s[1]
    t=t.split("\\")
    number = t[0]
    print(number)
