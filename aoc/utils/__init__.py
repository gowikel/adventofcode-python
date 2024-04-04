import os
from functools import lru_cache

from dotenv import dotenv_values
from rich.console import Console

console = Console()


@lru_cache(maxsize=None)
def load_config():
    return {**dotenv_values(), **os.environ}


config = load_config()
