import logging

import typer
from rich.console import Console
from rich.logging import RichHandler

from .utils.cli import validate_loglevel
from .utils.data import purge_cache

app = typer.Typer()
console = Console()
log = logging.getLogger(__name__)


@app.callback()
def main(level="INFO") -> None:
    """Main entry-point. Used to configure the app"""
    logging.basicConfig(
        level=validate_loglevel(level),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    log.info("Logging configured to {level}")


@app.command("clean-cache")
def clean_cache() -> None:
    """Deletes the stored cache"""
    with console.status("Cleaning..."):
        purge_cache()

    console.print("Cache cleaned!")


@app.command("solve")
def solve() -> None:
    """Attempts to solve the specifiec AOC challenge and use the results"""
    console.print("solve called")


if __name__ == "__main__":
    app()
