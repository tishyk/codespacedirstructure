# Simple server for return "Got: " + client msg
import pickle
from socket import *

def echo_server(address):
    con = socket(AF_INET, SOCK_STREAM)
    con.bind(address)
    con.listen(2)
    print('Server started..')
    while True:
        client, addr = con.accept()
        print("Connection from", addr)
        echo_handler(client)

def echo_handler(client):

    while True:
        data = client.recv(10000)
        try:
            load = pickle.loads(data)
            print(load)
        except EOFError:
            print('*', data)
        if not data:
            break
        client.sendall(data + b"Got: ")
    print("Connection closed")
    client.close()

if __name__ == "__main__":
    echo_server(('', 3002))