#!/usr/bin/env python
import sys

def deep_merge(a, b, level=0):
    '''Recursively merge 2 dicts a and b, go as deep as 9 levels.
    '''

    if level >= 9:
        return b
    else:
        level += 1

    # If neither a nor b is dict, no need to check further.
    if not isinstance(a, dict):
        return b
    if not isinstance(b, dict):
        return b

    for key in b:
        if key in a:
            a[key] = deep_merge(a[key], b[key])
        else:
            a[key] = b[key]

    return a


def two_level_split(line, sep=' ', quote='"'):
    '''Split a line by sep.

    The line may optionally contains fields that are quoted by the quote sign.
    '''

    in_quotes = False
    results = []
    temp = []

    for field in line.split(sep):
        if not field:
            results.append(field)
            continue

        if in_quotes:
            if field[0] == quote:
                raise ValueError(f"Non-matching `{quote}' quote: {line}")
            else:
                if field[-1] == quote:
                    temp.append(field.strip(quote))
                    results.append(sep.join(temp))
                    temp = []
                    in_quotes = False
                else:
                    temp.append(field)
        else:
            if field[0] == quote:
                if field[-1] == quote:
                    results.append(field.strip(quote))
                else:
                    in_quotes = True
                    temp.append(field.strip(quote))
            else:
                if field[-1] == quote:
                    raise ValueError(f"Non-matching `{quote}' quote: {line}")
                else:
                    results.append(field)

    return results
