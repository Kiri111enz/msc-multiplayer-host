from msc_multiplayer_host.settings import SETTINGS
import socket as sk


class Server:
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
            self.respond(client)

    @staticmethod
    def respond(client: sk.socket) -> None:
        message = client.recv(SETTINGS.message_size)
        client.sendall(message[::-1])
        client.close()


if __name__ == '__main__':
    Server().start()
