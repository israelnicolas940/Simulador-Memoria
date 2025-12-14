#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function
import click
from core.memsim import MemSim
import sys


@click.command()
def cli():
    """Cria e chama MemSim.

    Args:
        * None.

    Returns:
        None.
    """
    app = MemSim()
    sys.exit(app.cmdloop())


if __name__ == "__main__":
    cli()
