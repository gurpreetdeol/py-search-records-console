"""Top-level package for Ticket App"""
# __init__.py

__app_name__ = "Ticket"
__version__ = 1.0
__author__ = "Gurpreet Deol"
__email__ = "<EMAIL>"
__app_description__ = "Searching records from database using command-line"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    ID_ERROR: __app_name__ + " id Error",
}
