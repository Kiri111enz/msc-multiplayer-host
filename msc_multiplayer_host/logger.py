import os
from datetime import datetime
from settings import SETTINGS


def log(text: str) -> None:
    _append_to_file(SETTINGS.log_file_name, f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\t{text}\n')

    if SETTINGS.debug_mode:
        print(text)


def _append_to_file(file_name: str, text: str) -> None:
    with open(file_name, 'a+') as file:
        file.write(text)


def _set_up() -> None:
    logs_folder = os.path.dirname(SETTINGS.log_file_name)

    if logs_folder and not os.path.exists(logs_folder):
        os.makedirs(logs_folder, exist_ok=True)

    open(SETTINGS.log_file_name, 'w+').close()


_set_up()
