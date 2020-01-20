from socket import *
import pickle

load = {'a':1, 'b':2}
bload = pickle.dumps(load)
print(bload)
s = socket(AF_INET, SOCK_STREAM)

s.connect(('127.0.0.1', 3002)) # Connect
s.send(bload) # Send request
data = s.recv(10000) # Get response
s.close()