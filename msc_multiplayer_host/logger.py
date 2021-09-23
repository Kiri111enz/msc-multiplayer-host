from msc_multiplayer_host.settings import SETTINGS
import os
from datetime import datetime


def get_log_file_name() -> str:
    if not os.path.exists(SETTINGS.logs_folder):
        os.makedirs(os.path.dirname(SETTINGS.logs_folder), exist_ok=True)

    log_file_name = f'{SETTINGS.logs_folder}log_latest.txt'
    open(log_file_name, 'w+').close()

    return log_file_name


def log(file_name: str, text: str) -> None:
    _append_to_file(file_name, f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\t{text}\n')


def _append_to_file(file_name: str, text: str) -> None:
    with open(file_name, 'a+') as file:
        file.write(text)
