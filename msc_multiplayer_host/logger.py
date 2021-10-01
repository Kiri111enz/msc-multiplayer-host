import os
from datetime import datetime

LOGS_FOLDER = 'Logs/'
LOG_FILE_NAME = f'{LOGS_FOLDER}log_latest.txt'
DEBUG_MODE = True


def log(text: str) -> None:
    _append_to_file(LOG_FILE_NAME, f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\t{text}\n')

    if DEBUG_MODE:
        print(text)


def _append_to_file(file_name: str, text: str) -> None:
    with open(file_name, 'a+') as file:
        file.write(text)


def _set_up() -> None:
    if not os.path.exists(LOGS_FOLDER):
        os.makedirs(os.path.dirname(LOGS_FOLDER), exist_ok=True)

    open(LOG_FILE_NAME, 'w+').close()


_set_up()
