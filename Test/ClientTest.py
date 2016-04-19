import socket
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
p = GPIO.PWM(7, 100)
p.start(0)

s = socket.socket()
host = '10.0.0.5' # ip laptop
port = 12348
s.connect((host, port))
while True:
    text = (s.recv(1024))
    text = int(text)
    text = text + 50
    p.ChangeDutyCycle(text)
s.close()
