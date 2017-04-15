from socket import *
import time
 
arduinoAddress = ( '10.0.0.243', 5000)
arduinoSocket = socket(AF_INET, SOCK_DGRAM)
arduinoSocket.settimeout(1) #only wait 1 second for a resonse
count = 100

while(1): #Main Loop

    count += 1
    print(count)
    data = bytes(str(count), 'UTF-8')  #Set data to Blue Command
    arduinoSocket.sendto(data, arduinoAddress) #send command to arduino

 
    time.sleep(.1) #delay before sending next command