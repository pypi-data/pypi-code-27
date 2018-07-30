import time


def epoch(unit='s'):
    rate = {
        's': 1,
        'ms': 1000,
        'us': 10**6,
        'ns': 10**9,
    }
    return round(time.time()*rate[unit])
