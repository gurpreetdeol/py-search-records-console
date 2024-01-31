"""This module provides configuration functionality for Ticket App"""
# ticket/config.py

import configparser
from pathlib import Path
import typer

from ticket import (
    DB_WRITE_ERROR, DIR_ERROR, FILE_ERROR, SUCCESS, __app_name__
)

import base64

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"


def init_json_db(db_path: str) -> int:
    """Initialize JSON DB file"""
    config_code = _init_config_file()
    if config_code != SUCCESS:
        return config_code

    json_config = _create_json_db(db_path)
    if json_config != SUCCESS:
        return json_config
    return SUCCESS


def _init_config_file() -> int:
    """Initialize the app directory and file"""
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR

    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    return SUCCESS


def _create_json_db(db_path: str) -> int:
    """Create the json db file"""
    config_parser = configparser.ConfigParser()
    config_parser["General"] = {"database": db_path}
    try:
        with CONFIG_FILE_PATH.open("w") as file:
            config_parser.write(file)
    except OSError:
        return DB_WRITE_ERROR
    return SUCCESS


class DBConfiguration:
    SERVER: str = None
    DATABASE: str = None
    USERNAME: str = None
    PASSWORD: str = None
    PORT: int = 0
    IS_FOUND: bool = False
    ERROR_MESSAGE: str = None

    def __init__(self):
        try:
            config_parser = configparser.ConfigParser()
            config_parser.read(CONFIG_FILE_PATH)
            server_config = config_parser['SERVER']
            self.SERVER = base64.b64decode(server_config['host']).decode('utf-8')
            self.DATABASE = base64.b64decode(server_config['database']).decode('utf-8')
            self.PORT = int(base64.b64decode(server_config['port']).decode('utf-8'))
            self.USERNAME = base64.b64decode(server_config['username'.lower()]).decode('utf-8')
            self.PASSWORD = base64.b64decode(server_config['password'.lower()]).decode('utf-8')
            self.IS_FOUND = True
        except configparser.Error as err:
            self.ERROR_MESSAGE = str(err)
