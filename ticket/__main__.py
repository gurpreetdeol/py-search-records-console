"""TicketSearch App entry point."""
# ticket/__main__.py

from ticket import cli, __app_name__


def main():
    """Main entry point."""
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
