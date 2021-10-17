from collections import namedtuple

_Settings = namedtuple('Settings', ('port', 'log_file_name', 'debug_mode'))
SETTINGS = _Settings(25565, 'Logs/log_latest.txt', True)

_MessageId = namedtuple('MessageId', ('connected', 'disconnected'))
MESSAGE_ID = _MessageId(0, 1)
