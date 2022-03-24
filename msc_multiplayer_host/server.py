import socket as sk
import struct
from threading import Thread
from queue import Queue
from settings import SETTINGS, MESSAGE_ID, SAVE_ALERT
from socket_utils import get_socket, try_recv
import logger


class ThreadedServer:
    def __init__(self, port: int):
        self._socket = get_socket()
        self._socket.bind(('', port))

        self._socket_by_index = {}
        self._nickname_by_index = {}
        self._to_send_by_index = {}
        self._pending_indexes = [0]

    def start(self) -> None:
        logger.log('Server started.')
        self._socket.listen(5)

        while True:
            client, _ = self._socket.accept()
            Thread(target=self._handle_client, args=(client,)).start()

    def _handle_client(self, client: sk.socket) -> None:
        index = self._get_free_client_index()

        try:
            logger.log(f'Client {index} connected.')
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
        nickname_size = try_recv(client, 1)
        nickname = nickname_size + try_recv(client, struct.unpack('b', nickname_size)[0])
        client.send(struct.pack('2b', index, len(self._nickname_by_index)))
        self._socket_by_index[index] = client

        for client_index in self._to_send_by_index:
            self._to_send_by_index[client_index].put(struct.pack('2b', MESSAGE_ID.connected, index) + nickname)
            client.send(struct.pack('b', client_index) + self._nickname_by_index[client_index])

        self._nickname_by_index[index] = nickname
        self._to_send_by_index[index] = Queue()

    def _exchange_info_with_client(self, client: sk.socket, index: int) -> None:
        while True:
            message_size = try_recv(client, 1)

            if message_size == SAVE_ALERT:
                self._react_on_save_alert(index)
                continue

            message = try_recv(client, struct.unpack('b', message_size)[0])

            for client_index in self._to_send_by_index:
                if client_index != index:
                    self._to_send_by_index[client_index].put(message)

            while not self._to_send_by_index[index].empty():
                client.send(self._to_send_by_index[index].get())

    def _forget_client(self, client: sk.socket, index: int) -> None:
        client.close()

        try:
            del self._socket_by_index[index]
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

    def _react_on_save_alert(self, index_sent: int) -> None:
        if index_sent == 0:
            self._send_save_to_new_client()
            logger.log('Sent save to new client.')
        else:
            for client_index in self._socket_by_index:
                if client_index != index_sent:
                    self._socket_by_index[client_index].send(SAVE_ALERT)

            logger.log('New client loaded, told everyone to unpause.')

    def _send_save_to_new_client(self) -> None:
        host = self._socket_by_index[0]
        new_client = self._socket_by_index[list(self._socket_by_index.keys())[-1]]

        file_count = try_recv(host, 1)
        new_client.send(file_count)

        for _ in range(struct.unpack('b', file_count)[0]):
            file_size = struct.unpack('i', try_recv(host, 4))[0]

            while file_size > 0:
                chunk_size = min(8192, file_size)
                chunk = try_recv(host, chunk_size)
                new_client.send(chunk)
                file_size -= len(chunk)


if __name__ == '__main__':
    ThreadedServer(SETTINGS.port).start()
