from collections import namedtuple

_Settings = namedtuple('Settings', ('port', 'msg_connected_id', 'msg_disconnected_id',
                                    'log_file_name', 'debug_mode'))
SETTINGS = _Settings(25565, 0, 1,
                     'Logs/log_latest.txt', True)
