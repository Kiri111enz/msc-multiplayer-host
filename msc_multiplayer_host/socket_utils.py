import socket as sk


def get_socket() -> sk.socket:
    socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

    return socket


def try_recv(socket: sk.socket, size: int) -> bytes:
    message = socket.recv(size)

    if not message:
        raise ConnectionResetError('Connection closed!', socket)

    return message
