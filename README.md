## Advent of Code - Python

This is my repo storing my solutions to the Advent of Code challenges
in Python.

## Basic setup

Simply install poetry, then execute `poetry install --no-root`. That will
install all dependencies. If you want, you can exclude some groups:

- `--without=dev` will exclude development dependencies
- `--without=test` will exclude test dependencies
- `--without=dev,test` will exclude both

That's it really!

## Invoke

I am using [invoke](https://docs.pyinvoke.org/en/stable/index.html) as a friendly,
python based, command management system. It is listed as a dev dependency. Once
installed, you can invoke it as:

```bash
invoke fmt
```

Albeit, this project aims to be simple, which means that in most cases you are not
going to need it. For example, to run tests, just write `pytest`.

## Configuration

You need to use your Advento of Code Cookie session in order to be able to
download the puzzle input. Just store it on the `SESSION_COOKIE` env variable.

For convenience, the project reads the `.env` file.
