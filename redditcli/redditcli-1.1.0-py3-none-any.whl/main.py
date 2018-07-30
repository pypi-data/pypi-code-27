#!/usr/bin/env python3
from .redditcli import redditcli

def cli():
    r = redditcli()
    r.start()

if __name__ == "__main__":
    cli()
