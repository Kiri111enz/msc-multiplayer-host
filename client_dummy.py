from msc_multiplayer_host.settings import SETTINGS
import socket as sk
import click


@click.command()
@click.argument('host_address')
@click.argument('message')
def test(host_address: str, message: str) -> None:
    socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    socket.connect((host_address, SETTINGS.port))
    socket.settimeout(SETTINGS.timeout)

    socket.sendall(message.encode())

    while True:
        response = socket.recv(SETTINGS.message_size).decode()

        if not response:
            break

        open('test.txt', 'a').write(response)

    socket.close()


if __name__ == '__main__':
    test()
