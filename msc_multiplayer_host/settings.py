from collections import namedtuple
from enum import Enum

_Settings = namedtuple('Settings', ('port', 'log_file_name', 'debug_mode'))
SETTINGS = _Settings(25565,
                     'Logs/log_latest.txt', True)


class MessageType(Enum):
    CONNECTED = 0
    DISCONNECTED = 1
    INTRODUCTION = 2
    TRANSFORM_UPDATE = 3
