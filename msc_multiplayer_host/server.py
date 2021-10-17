from settings import SETTINGS, MESSAGE_ID
from socket_utils import get_socket, receive_message
import logger
import socket as sk
import struct
from threading import Thread
from queue import Queue


class ThreadedServer:
    def __init__(self, port: int):
        self._socket = get_socket()
        self._socket.bind(('', port))

        self._pending_indexes = [0]
        self._nickname_by_index = {}
        self._to_send_by_index = {}

    def start(self) -> None:
        logger.log('Server started.')
        self._socket.listen(5)

        while True:
            client, _ = self._socket.accept()
            Thread(target=self._handle_client, args=(client,)).start()

    def _handle_client(self, client: sk.socket) -> None:
        index = self._get_free_client_index()
        logger.log(f'Client {index} connected.')

        try:
            self._register_client(client, index)
            self._exchange_info_with_client(client, index)
        except ConnectionResetError:
            pass
        except Exception as exception:
            logger.log(repr(exception))
        finally:
            self._forget_client(client, index)

        logger.log(f'Client {index} disconnected.')

    def _register_client(self, client: sk.socket, index: int) -> None:
        nickname = receive_message(client)
        client.send(struct.pack('2b', index, len(self._nickname_by_index)))

        for client_index in self._to_send_by_index:
            self._to_send_by_index[client_index].put(struct.pack('2b', MESSAGE_ID.connected, index) + nickname)
            client.send(struct.pack('b', client_index) + self._nickname_by_index[client_index])

        self._nickname_by_index[index] = nickname
        self._to_send_by_index[index] = Queue()

    def _exchange_info_with_client(self, client: sk.socket, index: int) -> None:
        while True:
            message = receive_message(client)

            for client_index in self._to_send_by_index:
                if client_index != index:
                    self._to_send_by_index[client_index].put(message)

            while not self._to_send_by_index[index].empty():
                client.send(self._to_send_by_index[index].get())

    def _forget_client(self, client: sk.socket, index: int) -> None:
        client.close()

        try:
            del self._nickname_by_index[index]
            del self._to_send_by_index[index]
        except KeyError:
            pass

        self._pending_indexes.append(index)

        for client_index in self._to_send_by_index:
            self._to_send_by_index[client_index].put(struct.pack('2b', MESSAGE_ID.disconnected, index))

    def _get_free_client_index(self) -> int:
        new_client_index = min(self._pending_indexes)
        self._pending_indexes.remove(new_client_index)

        if not self._pending_indexes:
            self._pending_indexes.append(new_client_index + 1)

        return new_client_index


if __name__ == '__main__':
    ThreadedServer(SETTINGS.port).start()
