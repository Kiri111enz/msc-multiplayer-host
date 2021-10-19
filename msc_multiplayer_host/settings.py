from collections import namedtuple
import struct

_Settings = namedtuple('Settings', ('port', 'log_file_name', 'debug_mode'))
SETTINGS = _Settings(25565, 'Logs/log_latest.txt', True)

_MessageId = namedtuple('MessageId', ('connected', 'disconnected'))
MESSAGE_ID = _MessageId(0, 1)

SAVE_ALERT = struct.pack('b', 0)
