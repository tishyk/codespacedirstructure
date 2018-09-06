from socket import *
s = socket(AF_INET,SOCK_STREAM)
s.connect(("www.python.org",80)) # Connect
s.send("GET /index.html HTTP/1.0\n\n".encode()) # Send request
data = s.recv(10000) # Get response
s.close()