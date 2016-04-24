import socket
import smbus

bus = smbus.SMBus(1)
address = 0x04

s = socket.socket()
host = '10.0.0.5' # ip laptop
port = 12348
s.connect((host, port))

while True:
    text = (s.recv(1024))
    text = int(text)
    bus.write_byte(address, text)
s.close()
