from collections import namedtuple
from enum import Enum

_Settings = namedtuple('Settings', ('logs_folder', 'port', 'timeout'))


class MessageType(Enum):
    INTRODUCTION = 0
    TRANSFORM_UPDATE = 1


SETTINGS = _Settings('Logs/', 25565, 60)
MESSAGE_SIZES = {MessageType.INTRODUCTION.value: 20,
                 MessageType.TRANSFORM_UPDATE.value: 16}
