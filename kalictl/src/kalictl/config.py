import configparser, os
from pathlib import Path

import typer

from kalictl import (
    FILE_ERROR, DIR_ERROR, SUCCESS, __app_name__
)

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"

def add_config_entry(key: str, value: str, if_exists_ok = True) -> bool:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    if key in config['DEFAULT'] and if_exists_ok:
        return SUCCESS
    config['DEFAULT'][key] = value
    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)
    return SUCCESS

def init_app(username: str) -> int:
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code
    if not username.isalnum():
        return FILE_ERROR
    u_entry = add_config_entry('username', username)
    p_storage_path = Path(f"/Users/{os.getenv('USER')}/.kali")
    p_storage_path.mkdir(exist_ok=True)
    return SUCCESS if u_entry == SUCCESS else FILE_ERROR

def _init_config_file() -> int:
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    return SUCCESS

def get_config_entry(key: str) -> str:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    return config['DEFAULT'][key]