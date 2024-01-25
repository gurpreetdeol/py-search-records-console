"""The module provides the Ticket App model-controller functionality."""
# app/ticket.py

from pathlib import Path
from typing import (
    NamedTuple,
    Dict,
    List,
    Any
)
from ticket.json_db import JsonDBHandler
from ticket import (
    DB_READ_ERROR
)
from datetime import datetime


class CurrentTicket(NamedTuple):
    """"A Ticket model"""
    ticket: List[Dict[str, Any]]
    error: int


class AppLog(NamedTuple):
    """A Ticket App Log model"""
    log: List[Dict[str, Any]]
    error: int


class TicketLog:
    """The Ticket model"""

    def __init__(self, db_path: Path) -> None:
        self._json_db_handler = JsonDBHandler(db_path)

    def add_logs(self, *, log: str, priority: int = 1) -> AppLog:
        """Add a new Ticket App Log to the json file."""
        log_text = log.strip()
        # if not log_text.endswith("."):
        #     log_text += "."
        log_time = str(datetime.now())
        app_log = {
            "Log": log_text,
            "Priority": priority,
            "LogTime": log_time,
            "User": Path.home().stem
        }
        read = self._json_db_handler.read_logs()
        if read.error == DB_READ_ERROR:
            return AppLog(app_log, error=read.error)
        read.log.append(app_log)
        write = self._json_db_handler.write_log(read.log)
        return AppLog(app_log, error=write.error)

    def get_log_list(self) -> List[Dict[str, Any]]:
        """"Return the Ticket log list"""
        read = self._json_db_handler.read_logs()
        return read.log
