from collections import namedtuple

_Settings = namedtuple('Settings', ('logs_folder', 'port', 'message_size', 'timeout'))

SETTINGS = _Settings('Logs/', 25565, 4, 30)
