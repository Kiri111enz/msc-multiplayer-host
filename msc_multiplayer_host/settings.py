from collections import namedtuple

_Settings = namedtuple('Settings', ('port', 'message_size', 'timeout'))

SETTINGS = _Settings(10000, 1024, 300)
