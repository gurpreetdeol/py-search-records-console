"""This module provides the Ticket App CLI"""
# ticket/cli.py

from typing import (
    Optional,
    List
)

from rich.console import Console
from rich.table import Table

import typer
from pathlib import Path

from ticket import (
    __app_name__, __version__, json_db, ERRORS, config, ticket
)

app = typer.Typer()

console = Console()


@app.command(name="search")
def search(
        search_text: str,
):
    __add_log(search_text)
    typer.secho(
        f"Searching for {search_text}",
        fg=typer.colors.GREEN
    )
    if 1 == 1:
        msg = f"No records found for {search_text}"
        __add_log(msg, 2)
        typer.secho(message=msg,
                    fg=typer.colors.RED
                    )
        raise typer.Exit(1)


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


@app.command(name="logs")
def log_list_all() -> None:
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


@app.command(name="logs_plain")
def log_list_all_plain() -> None:
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
