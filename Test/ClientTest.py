import socket

s = socket.socket()
host = '10.0.0.5' # ip laptop
port = 12346
s.connect((host, port))
print(s.recv(1024))
s.close()
