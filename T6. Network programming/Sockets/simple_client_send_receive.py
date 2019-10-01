from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(("127.0.0.1", 9000))  # Connect
data = 1

while data:
    s.send("Get Hello!\n".encode())  # Send request
    data = s.recv(10000)  # Get response
    print(data)
