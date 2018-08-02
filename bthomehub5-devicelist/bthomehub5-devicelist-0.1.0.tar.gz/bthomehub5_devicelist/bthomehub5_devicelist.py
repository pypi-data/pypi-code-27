from html_table_parser import HTMLTableParser
import requests
import logging

_LOGGER = logging.getLogger(__name__)


def get_devicelist(home_hub_ip='192.168.1.254'):
    """Retrieve data from BT Home Hub 5 and return parsed result.
    """

    url = 'http://{}/'.format(home_hub_ip)

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        _LOGGER.exception("Connection to the router timed out")
        return
    if response.status_code == 200:
        return parse_devicelist(response.text)
    else:
        _LOGGER.error("Invalid response from Home Hub: %s", response)


def parse_devicelist(data_str):
    """Parse the BT Home Hub 5 data format."""

    p = HTMLTableParser()
    p.feed(data_str)

    known_devices = p.tables[9]

    devices = {}

    for device in known_devices:
        if len(device) == 5 and device[2] != '':
            devices[device[2]] = device[1]

    return devices
