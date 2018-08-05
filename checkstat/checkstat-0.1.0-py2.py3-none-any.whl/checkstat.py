import requests


def is_up(webpage):
    """Return True if 200 code was recieved, else return False."""
    try:
        req = requests.get(webpage)
    except requests.exceptions.ConnectionError:
        return False
    else:
        if req.status_code == 200:
            return True
        return False
