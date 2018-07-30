#!/usr/bin/env python3
from .rdt_cli import rdt_cli

def cli():
    r = rdt_cli()
    r.begin()

if __name__ == "__main__":
    cli()
