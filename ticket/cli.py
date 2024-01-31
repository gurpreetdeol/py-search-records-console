"""This module provides the Ticket App CLI"""
# ticket/cli.py

from typing import (
    Optional,
    List
)

from rich.console import Console
from rich.table import Table, Column
from rich import box

import typer
from pathlib import Path

from ticket import (
    __app_name__, __version__, json_db, ERRORS, config, ticket, database
)

import pandas as pd

app = typer.Typer()

console = Console()


@app.command(name="search")
def search(ticket_number: Optional[int] = typer.Option(
    None,  #
    "--search",
    "-s",
    prompt="Ticket#: ?"
),
):
    """Search for Ticket details by Ticket Number"""
    __add_log(str(ticket_number))
    __ticket_number: int = 0
    try:
        __ticket_number = int(ticket_number)
    except ValueError:
        typer.secho(
            f"Invalid Ticker Number {__ticket_number}.",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    db = database.Database()
    if db.IS_CONNECTED:
        records = db.search(__ticket_number)
        __display_ticket_info(__ticket_number, records)
        if len(records) == 0:
            msg = f"No records found for {__ticket_number}"
            __add_log(msg, 2)
            typer.secho(message=msg,
                        fg=typer.colors.RED
                        )
            raise typer.Exit(1)
    else:
        __add_log(db.ERROR_MESSAGE, 1)
        typer.secho(message=db.ERROR_MESSAGE,
                    fg=typer.colors.RED
                    )
        raise typer.Exit(1)


def __display_ticket_info(__ticket_number, records):
    __table_title = f"Customer Ticket #{__ticket_number} Details"
    table = Table(Column(header="id", min_width=11),  # 0
                  Column(header="description"),  # 1
                  Column(header="req-id", min_width=11),  # 2
                  Column(header="req-name"),  # 3
                  Column(header="req-status-name"),  # 4
                  Column(header="resp-id"),  # 5
                  Column(header="resp-name"),  # 6
                  Column(header="status"),  # 7
                  Column(header="urgent"),  # 8
                  Column(header="source"),  # 9
                  # Column(header="source-name"),  # 10
                  Column(header="spam"),  # 11
                  Column(header="deleted"),  # 12
                  Column(header="created-at"),  # 13
                  Column(header="updated-at"),  # 14
                  Column(header="trained"),  # 15
                  Column(header="subject"),  # 16
                  Column(header="display-id"),  # 17
                  Column(header="due-by"),  # 18
                  # Column(header="frDueBy"),  # 19
                  Column(header="is_escal."),  # 20
                  Column(header="priority"),  # 21
                  # Column(header="priority-name"),  # 22
                  Column(header="fr-escal."),  # 23
                  Column(header="to-email", min_width=20),  # 24
                  # Column(header="delta"),  # 25
                  Column(header="ticket-type"),  # 26
                  title="Customer Ticket Details",
                  expand=True)

    for index, log in enumerate(records, 1):
        email_to = str(log[24]).split("@")
        email_to_ext = email_to[1].split('.')
        email_to_domain_full = "\n.".join(list(email_to_ext))
        table.add_row(str(int(log[0])),
                      str(log[1]),
                      str(int(log[2])),
                      str(log[3]),
                      str(log[4]),
                      str(log[5]),
                      str(log[6]),
                      str(log[7]),
                      str(log[8]),
                      f"{str(log[9])}. {str(log[10])}",
                      str(log[11]),
                      str(log[12]),
                      str(log[13]).split("T")[0],
                      str(log[14]).split("T")[0],
                      str(log[15]),
                      str(log[16]),
                      str(log[17]),
                      str(log[18]).split("T")[0],
                      # str(log[19]),
                      str(log[20]),
                      f"{str(log[21])}. {str(log[22])}",
                      str(log[23]),
                      f"{email_to[0]}\n@{str(email_to_domain_full)}",
                      # f"{email_to[0]}\n@{email_domain}\n.{email_to_ext}",
                      # str(log[25]),
                      str(log[26]))

    console.print(table)


@app.command(name="config")
def config_path(config_search: Optional[str] = typer.Option(
    "",
    "--config",
    "-c"
),
):
    """Get back configuration file path"""
    typer.secho(f"Configuration file path: {config.CONFIG_FILE_PATH}", fg=typer.colors.BLACK)


@app.command()
def init(db_path: str = typer.Option(
    str(json_db.DEFAULT_JSON_DB_PATH),
    "--log-path",
    "-lp",
    prompt="Ticket logs file location?"
),
) -> None:
    """Initialize the Ticket database."""
    app_init_error = config.init_json_db(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS(app_init_error)}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    db_init_error = json_db.init_json_db(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating logs file failed with "{ERRORS(db_init_error)}"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The Ticket App logs file is {db_path}", fg=typer.colors.GREEN)


def get_logs() -> ticket.TicketLog:
    if config.CONFIG_FILE_PATH.exists():
        db_path = json_db.get_json_db_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found, please run ticket init first',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    if db_path.exists():
        return ticket.TicketLog(db_path)
    else:
        typer.secho(
            'Log DB file not found, please run ticket init first',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)


def __add_log(log: str, priority: int = 1) -> None:
    """Add a new Ticket App with DESCRIPTION."""
    ticket_log = get_logs()
    log_text, error = ticket_log.add_logs(log=log, priority=priority)
    if error:
        typer.secho(
            f'Adding Log failed with "{ERRORS[error]}"',
            fg=typer.colors
        )
        raise typer.Exit(1)
    # else:
    #     typer.secho(
    #         f"""Log: "{log_text["Log"]}" was successfully added """,
    #         fg=typer.colors.GREEN
    #     )


@app.command(name="logs", short_help="List all Ticket logs")
def log_list_all(search_log: Optional[str] = typer.Option(
    "",
    "--logs",
    "-l"
), ) -> None:
    """List all Ticket logs"""
    ticket_log = get_logs()
    log_list = ticket_log.get_log_list()
    if len(log_list) == 0:
        typer.secho(
            f"There is no log in the Ticket App yet.", fg=typer.colors.RED
        )
        raise typer.Exit(1)
    typer.secho("\nTicket App logs:", bold=True, fg=typer.colors.BLUE)
    table = Table("ID.", "Priority", "LogTime", "Log", "User")
    for id, log in enumerate(log_list, 1):
        desc, priority, log_time, user = log.values()
        table.add_row(str(id), str(priority), str(log_time), desc, user)
    console.print(table)


@app.command(name="logs_plain", short_help="List all Ticket logs in plain text")
def log_list_all_plain(search_log: Optional[str] = typer.Option(
    "",
    "--logs_plain",
    "-lp"
), ) -> None:
    """List all Ticket logs in plain"""
    ticket_log = get_logs()
    log_list = ticket_log.get_log_list()
    if len(log_list) == 0:
        typer.secho(
            f"There is no log in the Ticket App yet.", fg=typer.colors.RED
        )
        raise typer.Exit(1)
    typer.secho("\nTicket App logs:", bold=True, fg=typer.colors.BLUE)
    columns = (
        "ID.   ",
        "| Priority  ",
        "| LogTime  ",
        "| Log  "
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id, todo in enumerate(log_list, 1):
        desc, priority, log_time = todo.values()
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id)) - 1) * ' '}"
            f" | ({priority}){(len(columns[1]) - len(str(priority)) - 5) * ' '}"
            f" | {log_time}{(len(columns[2]) - len(str(log_time)) - 2) * ' '}"
            f"| {desc}",
            fg=typer.colors.BLUE
        )

    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the Ticket App version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return
