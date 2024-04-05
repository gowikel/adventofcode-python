import os

from dotenv import dotenv_values


def load_config():
    return {**dotenv_values(), **os.environ}


config = load_config()
