# Simple server for return "Got: " + client msg

from socket import *
import threading

def echo_server(address):
    con = socket(AF_INET, SOCK_STREAM)
    con.bind(address)
    con.listen(1)
    while True:
        client, addr = con.accept()
        print("Connection from", addr)
        client_thread = threading.Thread(target=echo_handler, args=(client,), name=addr)
        client_thread.start()

def echo_handler(client):
    while True:
        data = client.recv(10000)
        if not data:
            break
        client.sendall(b"Got: " + data)
    print("Connection closed")
    client.close()

if __name__ == "__main__":
    echo_server(('', 9000))