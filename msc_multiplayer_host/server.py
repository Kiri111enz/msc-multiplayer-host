from msc_multiplayer_host.settings import SETTINGS, MessageType, MESSAGE_SIZES
import msc_multiplayer_host.logger as logger
import socket as sk
import threading
import struct
from queue import Queue


class ThreadedServer:
    def __init__(self):
        self._socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self._socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        self._socket.bind(('', SETTINGS.port))

        self._pending_indexes = [0]
        self._nickname_by_index = {}
        self._to_send_by_index = {}

        self._log_file_name = logger.get_log_file_name()

    def start(self) -> None:
        logger.log(self._log_file_name, 'Server started.')
        self._socket.listen(5)

        while True:
            client, _ = self._socket.accept()
            threading.Thread(target=self._handle_client, args=(client,)).start()

    def _handle_client(self, client: sk.socket) -> None:
        index = self._get_free_client_index()
        logger.log(self._log_file_name, f'Client {index} connected.')

        self._register_client(client, index)
        self._exchange_info_with_client(client, index)
        self._forget_client(client, index)

        logger.log(self._log_file_name, f'Client {index} disconnected.')

    def _register_client(self, client: sk.socket, index: int) -> None:
        for client_index in self._to_send_by_index:
            self._to_send_by_index[client_index].put(struct.pack('2b', MessageType.CONNECTED.value, index))

        nickname = client.recv(MESSAGE_SIZES[MessageType.INTRODUCTION.value])
        client.send(struct.pack('b', index))
        client.send(struct.pack('b', len(self._nickname_by_index)))

        for client_index in self._nickname_by_index:
            client.send(struct.pack('b', client_index) + self._nickname_by_index[client_index])

        self._nickname_by_index[index] = nickname
        self._to_send_by_index[index] = Queue()

    def _exchange_info_with_client(self, client: sk.socket, index: int) -> None:
        while True:
            try:
                message_type = client.recv(1)
            except ConnectionResetError:
                break

            if not message_type:
                break

            message = message_type + client.recv(MESSAGE_SIZES[struct.unpack('b', message_type)[0]])

            for client_index in self._to_send_by_index:
                if client_index != index:
                    self._to_send_by_index[client_index].put(message)

            while not self._to_send_by_index[index].empty():
                message = self._to_send_by_index[index].get()
                client.send(message)

    def _forget_client(self, client: sk.socket, index: int) -> None:
        client.close()

        del self._nickname_by_index[index]
        del self._to_send_by_index[index]
        self._pending_indexes.append(index)

        for client_index in self._to_send_by_index:
            self._to_send_by_index[client_index].put(struct.pack('2b', MessageType.DISCONNECTED.value, index))

    def _get_free_client_index(self) -> int:
        new_client_index = min(self._pending_indexes)
        self._pending_indexes.remove(new_client_index)

        if not self._pending_indexes:
            self._pending_indexes.append(new_client_index + 1)

        return new_client_index


if __name__ == '__main__':
    ThreadedServer().start()
