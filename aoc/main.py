import logging
import sys

from rich.console import Console
from rich.logging import RichHandler
from .utils.cli import parse_args
from .utils.data import download_input

FORMAT = "%(message)s"

console = Console()
log = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        level="NOTSET",
        format=FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    cli_opts = parse_args(sys.argv[1:])
    console.print("Parse conf:", cli_opts)

    try:

        year = 2023
        day = 1

        input_data = download_input(year, day)
        console.print(input_data)
    except Exception as exc:
        log.exception(f"Execution failed: {exc}")


if __name__ == "__main__":
    main()
