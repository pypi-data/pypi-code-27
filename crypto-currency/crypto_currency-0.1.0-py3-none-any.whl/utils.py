# Code By Vaayne
import datetime
import logging

import requests


def get_logger():
    logger = logging.getLogger('coin')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    # fh = logging.FileHandler('coin.log')
    # fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    # logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


logger = get_logger()


def timestamp_to_date(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp)


def fetch_data(url, **kwargs):
    """
    Use get method to fetch url
    Args:
        url(str): full URL
        **kwargs: other args

    Returns:
        JSON return data
    """
    logger.debug('Calling URL - %s', url)
    r = requests.get(url, **kwargs)
    if r.status_code == 200:
        return r.json()
    logger.error(f"Get {url} Error. Error code: {r.status_code}, Message:  {r.json()}")
