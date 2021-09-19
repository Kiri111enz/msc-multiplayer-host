from msc_multiplayer_host.settings import SETTINGS
import socket as sk
import threading
import struct


class ThreadedServer:
    def __init__(self):
        self.socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

        host_address = sk.gethostbyname(sk.gethostname())
        print(host_address)
        self.socket.bind((host_address, SETTINGS.port))

    def start(self) -> None:
        self.socket.listen(5)

        while True:
            client, _ = self.socket.accept()
            client.settimeout(SETTINGS.timeout)
            threading.Thread(target=self._talk_with_client, args=(client,)).start()

    @staticmethod
    def _talk_with_client(client: sk.socket) -> None:
        print(f'Connected from {client}.')
        client.settimeout(SETTINGS.timeout)

        while True:
            x, y, z, rot_y = [client.recv(SETTINGS.message_size) for _ in range(4)]

            if not x:
                break

            x, y, z, rot_y = (struct.unpack('f', value) for value in (x, y, z, rot_y))

            print(f'{x} {y} {z}  {rot_y}')

        print(f'Closing connection with {client}.')
        client.close()


if __name__ == '__main__':
    ThreadedServer().start()
