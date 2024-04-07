import os

from dotenv import dotenv_values


def load_config():
    """Loads configuration from both, the dotenv file and the environ"""
    return {**dotenv_values(), **os.environ}


config = load_config()
