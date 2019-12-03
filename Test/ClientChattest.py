import socket

s = socket.socket()
host = '172.16.0.2'
port = 12221

s.connect((host, port))
print('Connected to', host)

while True:
    z = "Enter something for the server: "
    s.send(bytes(z, 'UTF-8'))
    # Halts
    print('[Waiting for response...]')
    print(s.recv(1024))
