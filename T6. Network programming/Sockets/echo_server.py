# Simple server for return "Got: " + client msg

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
        print('*', data)
        if not data:
            break
        client.sendall(b"Got: " + data)
    print("Connection closed")
    client.close()

if __name__ == "__main__":
    echo_server(('', 8080))