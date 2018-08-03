"""Utilities for dealing with sqlite."""
import re
import sqlite3


def regexp(expr, item):
    """Regex function for sqlite."""
    reg = re.compile(expr)
    return reg.search(item) is not None


def db_connect(db_path):
    """Return sqlite connection object."""
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    con.create_function('REGEXP', 2, regexp)
    return con
