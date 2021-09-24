from collections import namedtuple
from enum import Enum

_Settings = namedtuple('Settings', ('logs_folder', 'port'))
SETTINGS = _Settings('Logs/', 25565)


class MessageType(Enum):
    CONNECTED = 0
    DISCONNECTED = 1
    INTRODUCTION = 2
    TRANSFORM_UPDATE = 3


MESSAGE_SIZES = {MessageType.INTRODUCTION.value: 20,
                 MessageType.TRANSFORM_UPDATE.value: 17}
