from invoke import task


@task
def isort(c):
    """Sorts the imports"""
    c.run("isort .")


@task
def black(c):
    """Formats the source code using black"""


@task(pre=[black, isort])
def fmt(c):
    """Format the source code files"""
    pass
