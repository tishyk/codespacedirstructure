# Simple server for return "Got: " + client msg

from socket import *
import asyncio
from pprint import  pprint

async def echo_server(address, loop):
    con = socket(AF_INET, SOCK_STREAM)
    con.bind(address)
    con.listen(2)
    con.setblocking(False)
    print('Server started..')

    while True:
        client, addr = await loop.sock_accept(con)
        print("Connection from", addr)
        future = loop.create_task(echo_handler(client))

async def echo_handler(client):
    while True:
        if not loop.is_closed():
            data = await loop.sock_recv(client, 10000)
            pprint(data)
            asyncio.wait(print(i) for i in range(50000))
            if not data:
                break
            await loop.sock_sendall(client, b"Got: " + data)
    print("Connection closed")
    client.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(echo_server(('', 9000), loop))
