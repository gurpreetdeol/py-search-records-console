"""This module provides a database functionality for Ticket App"""
import configparser
# ticket/database.py

import json
from pathlib import Path
from typing import (
    NamedTuple,
    List,
    Dict,
    Any
)

from ticket import (
    SUCCESS,
    DB_WRITE_ERROR,
    DB_READ_ERROR,
    JSON_ERROR
)

from datetime import datetime, date

DEFAULT_JSON_DB_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_ticket.json"
)


def get_json_db_path(config_path) -> Path:
    """Return the current json path for the Ticket App database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_path)
    return Path(config_parser["General"]["database"])


def init_json_db(config_path: Path) -> int:
    """Initialize json database"""
    try:
        if not config_path.exists():  # if file does not exists the create one
            config_path.write_text("[]")  # Create a ticket logs file
    except OSError:
        return DB_WRITE_ERROR


# Define a custom function to serialize datetime objects
def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


class JsonDBResponse(NamedTuple):
    log: List[Dict[str, Any]]
    error: int


class JsonDBHandler:
    """Handles the Ticket App database."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def read_logs(self) -> JsonDBResponse:
        """Read the Ticket App logs from json file"""
        try:
            with self.db_path.open("r") as db:
                try:
                    return JsonDBResponse(json.load(db), SUCCESS)
                except Exception as ex:  # json.JSONDecodeError:
                    print(str(ex))
                    return JsonDBResponse([], DB_READ_ERROR)
        except OSError:  # catch file IO problem
            return JsonDBResponse([], DB_READ_ERROR)

    def write_log(self, logs: List[Dict[str, Any]]) -> JsonDBResponse:
        """Write the Ticket App logs to json file"""
        try:
            with self.db_path.open("w") as db:
                json.dump(logs, db, indent=4, default=serialize_datetime)
            return JsonDBResponse(logs, SUCCESS)
        except OSError:
            return JsonDBResponse(logs, DB_WRITE_ERROR)
