import serial

ser = serial.Serial("/dev/ttyACM0", 9600, timeout=None)
while True:
    message = "5"
    ser.write(message.encode())

    s = str(ser.readline(1))
    s=s.split("'")
    t=s[1]
    t=t.split("\\")
    number = t[0]
    print(number)