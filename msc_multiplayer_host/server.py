from msc_multiplayer_host.settings import SETTINGS, MessageType, MESSAGE_SIZES
import msc_multiplayer_host.logger as logger
import socket as sk
import threading
import struct


class ThreadedServer:
    def __init__(self):
        self._socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self._socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        self._socket.bind(('', SETTINGS.port))

        self._log_file_name = logger.get_log_file_name()

    def start(self) -> None:
        logger.log(self._log_file_name, 'Server started.')

        self._socket.listen(5)

        while True:
            client, _ = self._socket.accept()
            client.settimeout(SETTINGS.timeout)
            threading.Thread(target=self._talk_with_client, args=(client,)).start()

    def _talk_with_client(self, client: sk.socket) -> None:
        logger.log(self._log_file_name, f'Connected from {client}')

        while True:
            message_type = struct.unpack('h', client.recv(2))[0]

            if message_type == MessageType.INTRODUCTION.value:
                message = client.recv(MESSAGE_SIZES[MessageType.INTRODUCTION])
                nickname = struct.unpack(f'{len(message)}s', message)
                print(nickname)
            elif message_type == MessageType.TRANSFORM_UPDATE.value:
                # x, y, z, rot_y = struct.unpack('4f', client.recv(MESSAGE_SIZES[MessageType.TRANSFORM_UPDATE]))
                x, y, z, rot_y = (struct.unpack('f', value) for value in [client.recv(4) for _ in range(4)])
                print(f'{x} {y} {z}  {rot_y}')

        # noinspection PyUnreachableCode
        logger.log(self._log_file_name, f'Closing connection with {client}.')
        client.close()


if __name__ == '__main__':
    ThreadedServer().start()
