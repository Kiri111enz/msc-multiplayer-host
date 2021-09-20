from msc_multiplayer_host.settings import SETTINGS, MESSAGE_SIZES
import msc_multiplayer_host.logger as logger
import socket as sk
import threading
import struct


class ThreadedServer:
    def __init__(self):
        self._socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self._socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        self._socket.bind(('', SETTINGS.port))

        self.pending_indexes = [0]
        self.to_send_by_index = {}
        self._log_file_name = logger.get_log_file_name()

    def start(self) -> None:
        logger.log(self._log_file_name, 'Server started.')
        self._socket.listen(5)

        while True:
            client, _ = self._socket.accept()
            client.settimeout(SETTINGS.timeout)
            threading.Thread(target=self._talk_with_client, args=(client, self._get_free_client_index())).start()

    def _talk_with_client(self, client: sk.socket, index: int) -> None:
        logger.log(self._log_file_name, f'Connected from {client}')
        self.to_send_by_index[index] = []

        while True:
            message_type = struct.unpack('h', client.recv(2))[0]
            message = client.recv(MESSAGE_SIZES[message_type])

            # TODO: add some thread safety

            for client_index in self.to_send_by_index.keys():
                if client_index != index:
                    self.to_send_by_index[client_index].append(message)

            for message in self.to_send_by_index[index]:
                client.send(message)

            self.to_send_by_index.clear()

        # noinspection PyUnreachableCode
        logger.log(self._log_file_name, f'Closing connection with {client}.')
        client.close()
        self.pending_indexes.insert(0, index)

    def _get_free_client_index(self) -> int:
        new_client_index = self.pending_indexes[0]
        self.pending_indexes.pop(0)

        if not self.pending_indexes:
            self.pending_indexes.append(new_client_index + 1)

        return new_client_index


if __name__ == '__main__':
    ThreadedServer().start()
