"""This module provides the TicketSearch App CLI"""
# ticket/cli.py

from typing import Optional

import typer

from ticket import __app_name__, __version__

app = typer.Typer()


@app.command(name="search")
def search(
        search_text: str  # = typer.Option("", "--search", "-s", min=6, max=10),
):
    typer.secho(
        f"Searching for {search_text}",
        fg=typer.colors.GREEN
    )


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
            help="Show the TicketSearch App version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return
