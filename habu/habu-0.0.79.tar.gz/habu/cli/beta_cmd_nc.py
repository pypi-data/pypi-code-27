import logging
from time import sleep
import asyncio

import click

#logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

#from scapy.all import ICMP, IP, conf, sr1, L3RawSocket

get_request = b'HEAD / HTTP/1.0\r\n\r\n'

async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 5000, loop=loop)

    while True:
        #print('Send: %r' % message)
        a = input('> ')
        writer.write(a.encode())

        data = await reader.read(100)
        print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()

@click.command()
@click.argument('ip')
@click.argument('port')
def cmd_nc(ip, port):

    message = 'Hello World!'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client(message, loop))
    loop.close()


if __name__ == '__main__':
    cmd_nc()
