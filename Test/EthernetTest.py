data = None
from socket import *
import select

timeout = 3 # timeout in seconds
msg = "test"

host = "10.0.0.11"
print ("Connecting to " + host)

port = 23

s = socket(AF_INET, SOCK_STREAM)
print("Socket made")

ready = select.select([s],[],[],timeout)


s.connect((host,port))
print("Connection made")


if ready[0]:        #if data is actually available for you
    print("[INFO] Sending message...")
    s.send(bytes("12345", 'UTF-8'))
    print("[INFO] Message sent.")

    data = s.recv(4096)
    print("[INFO] Data received")
    print(data)