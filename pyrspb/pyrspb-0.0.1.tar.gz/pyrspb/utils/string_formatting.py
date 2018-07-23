import re


def percent_str_to_float(s):
    return round(float(re.match("""(\d+\.?\d*)""", s).group(0)) / 100.0, 2)


def make_int(s):
    return int(s.replace(',', ''))


def make_float(s):
    return float(s.replace(',', ''))


def maybe_make_int(s):
    try:
        return make_int(s)
    except ValueError:
        return -1
