# pylint: disable=C0103
""" Sample ExoEdge application

This module provides utilities for simulating data to enable a quick-start
experience with ExoEdge and the IIoT solution ExoSense.
"""
from __future__ import print_function
import time
import random
import threading
import logging
import math
import json
import re


def fourteen():
    """ Return 14 """
    return 14


def current_time():
    """ Return the current timestamp """
    return time.time()


def echo(value=''):
    """ Echo a value into a string

    Parameters:
    value:          The value to be echoed
    """
    return str(value)


def strip_non_numeric(value=''):
    """ Strip out non-numeric characters from string

    Parameters:
    value:          The value to be stripped to numeric values
    """
    return int(re.sub('[^0-9]', '', value))


def sin_wave(period=60, amplitude=1, offset=0, precision=2):
    """ Generate a sin wave from the current time

    Parameters:
    period:         The period, in seconds, of the sin wave
    amplitude:      The amplitude of the sin wave
    offset:         The vertical offset of the sin wave
    """
    ratio = (time.time() % period) / period
    return round(math.sin(2 * math.pi * ratio) * amplitude + offset, precision)


def cos_wave(period=60, amplitude=1, offset=0, precision=2):
    """ Generate a sin wave from the current time

    Parameters:
    period:         The period, in seconds, of the cos wave
    amplitude:      The amplitude of the cos wave
    offset:         The vertical offset of the cos wave
    """
    ratio = (time.time() % period) / period
    return round(math.cos(2 * math.pi * ratio) * amplitude + offset, precision)


def location(latitude=None, longitude=None, period=60, radius=0.1, precision=6):
    """ Generate location data from the current time and a starting location

    Moves in a circle every `period` seconds. Path is `radius` decimal degrees
    from the center point defined by `latitude` and `longitude`.

    Parameters:
    latitude:       The latitude of the center point, in decimal degrees
    longitude:      The longitude of the center point, in decimal degrees
    period:         The period, in seconds, it takes to traverse the path
    radius:         The radius, in decimal degrees, of the path from the center
    """
    lat = sin_wave(period=period,
                   amplitude=radius,
                   offset=latitude,
                   precision=precision)
    lng = cos_wave(period=period,
                   amplitude=radius,
                   offset=longitude,
                   precision=precision)
    return json.dumps({'lat': lat, 'lng': lng})


def random_integer(lower=0, upper=10):
    """ Get a random integer between two values

    Parameters:
    lower:          The lower bound of the random number
    upper:          The upper bound of the random number
    """
    return random.randint(lower, upper)


def random_sleep_1(_fn=None, event=None, lower=1, upper=10):
    """ Start AsyncSim thread.

    The two parameters `_fn` and `event` are protected and overwritten
    by exoedge.channel.Channel

    Parameters:
    lower:          The lower bound of the sleep time, in seconds
    upper:          The upper bound of the sleep time, in seconds
    """
    AsyncSim(_fn, event, lower, upper).start()


class AsyncSim(threading.Thread):
    """ Minimal class to simulate a threaded source """
    def __init__(self, f, e, lower, upper):
        """
        Initialized by async(). For this example, setDaemon is used so that,
        if the channel that created this thread is killed, the AsyncSim thread
        will also die.
        """
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self._fn = f
        self.event = e
        self.lower = lower
        self.upper = upper

    def run(self):
        """ Sleep for a random number of seconds

        After the thread has slept, set an event passed by its owner Channel.
        """
        logging.info('starting')
        while True:
            r = random.randint(self.lower, self.upper)
            logging.info('sleeping %ss', r)
            time.sleep(r)
            self._fn(current_time())
            self.event.set()


def random_sleep_2(lower=1, upper=10):
    """ Sleep for a random number of seconds

    Distinct from random_sleep_1 in that there is no additional thread
    required to get a value into the Channel. Instead, it merely returns when
    the sleep is done.

    Parameters:
    lower:          The lower bound of the sleep time, in seconds
    upper:          The upper bound of the sleep time, in seconds
    """
    r = random.randint(lower, upper)
    logging.info('sleeping %ss', r)
    time.sleep(r)
    return current_time()
