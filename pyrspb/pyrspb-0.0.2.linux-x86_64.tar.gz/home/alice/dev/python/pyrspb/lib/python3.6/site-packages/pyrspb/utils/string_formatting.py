import re


def percent_str_to_float(s):
    try:
        res = re.match("""(\d+\.?\d*)""", s)
        if res is not None:
            return round(float(res.group(0)) / 100.0, 2)
        else:
            return -1
    except TypeError:
        return -1


def make_float(s):
    try:
        return float(s.replace(',', ''))
    except ValueError:
        return -1


def make_int(s):
    try:
        return int(s.replace(',', ''))
    except ValueError:
        return -1
