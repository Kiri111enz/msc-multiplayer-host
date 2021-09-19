from collections import namedtuple

_Settings = namedtuple('Settings', ('port', 'message_size', 'timeout'))

SETTINGS = _Settings(25565, 4, 30)
