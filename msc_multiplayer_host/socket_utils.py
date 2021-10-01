import socket as sk


def get_socket() -> sk.socket:
    socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    socket.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

    return socket
