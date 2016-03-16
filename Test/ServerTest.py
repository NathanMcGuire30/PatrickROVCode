import socket

s = socket.socket()
host = '10.0.0.5' #My IP
port = 12346
s.bind((host, port))

s.listen(5)
while True:
  c, addr = s.accept()
  print('Got connection from', addr)
  c.send(bytes('hi', 'UTF-8'))
  c.close()