import socket as sk
import struct


def get_socket() -> sk.socket:
    socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

    return socket


def receive_message(socket: sk.socket) -> bytes:
    message_size = socket.recv(1)

    if not message_size:
        raise ConnectionResetError(f'Connection closed!', socket)

    return socket.recv(struct.unpack('b', message_size)[0])
