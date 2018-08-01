import os
import logging
import requests
from functools import partial


def _api(host, port, logger, req, params={}, **kwargs):
    try:
        api_url = 'http://{}{}/{}'.format(host, ':{}'.format(port) if port else '', req)
        response = requests.get(api_url, params=params, **kwargs)
        code = response.status_code
        req_msg = '[{}] API request to {}:'.format(code, response.url)
        if code == 200:
            logger.info('{} Successful response!'.format(req_msg))
            return response.json()
        else:
            if code >= 500:
                msg = 'Server Error'
            elif code == 404:
                msg = 'URL not found'
            elif code == 401:
                msg = 'Authentication Failed'
            elif code == 400:
                msg = 'Bad Request'
            elif code >= 300:
                msg = 'Unexpected Redirect'
            logger.error('{} {}'.format(req_msg, msg))
            return None
    except requests.exceptions.ConnectionError:
        logger.exception('Connection error')
        return None

def api(host, port= '', logger=None, api_token=None):
    logging.basicConfig(level=logging.ERROR)
    logger = logger or logging.getLogger(__name__)
    return partial(_api,
        os.environ.get(str(host), host),
        os.environ.get(str(port), port),
        logger,
        headers= {
            **{'Content-Type': 'application/json'},
            **({'Authorization': 'Bearer {}'.format(api_token)} if api_token else {})
        }
    )
