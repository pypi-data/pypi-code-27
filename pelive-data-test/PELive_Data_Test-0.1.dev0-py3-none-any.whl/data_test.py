import requests
from requests_negotiate_sspi import HttpNegotiateAuth
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from typing import List, Dict, Tuple, Union
import urllib3
import pandas as pd

# Set Max Retries to 5
s = requests.Session()
retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504])
s.mount('https://', HTTPAdapter(max_retries=retries))

# Suppress invalid cert warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://pelive.gic.com.sg/"

request_args = {
    'auth': HttpNegotiateAuth(),
    'proxies': {'http': None, 'https': None},
    'verify': False
}


def fetch(values: List[str],
          broken_down_by: List[str],
          filters: List[Tuple[str, str]]=[],
          cube_url=f"{base_url}/cube/api/v1/CUBE"):
    """Calls the PELive API to fetch investment data based on the supplied parameters

    Keyword Arguments:
        values (List[str]): Strings that describe what numerical values
            to fetch. Possible strings can be imported from `data_test.measures`

            Examples include `crp`, `DPI`, `IRR` ec

        broken_down_by (List[str]): Dimensions that measures will be broken
            down by

            Example

            ```
            import data_test.dimensions as D

            broken_down_by = [
                D.investmentGroup,
                D.companyName,
                D.investmentCountry
            ]
            ```

        filters (List[Tuple[str, str]]: Dictionary where:

            * key - dimension
            * value - Value to filter dimension on

            Example

            import data_test.dimensions as D

            filters = [
                (D.investmentGroup, 'Alibaba',
                (D.investmentCountry, 'China')
            ]
    """

    assert len(
        values) > 0, "You must include at least 1 measure, i.e. [M.IRR, M.DPI]"
    assert len(
        broken_down_by) > 0, "You must include at least 1 dimension, i.e. [D.investentGroup]"

    params = {
        'measures': ''.join(values),
        'dimensions': ''.join(broken_down_by)
    }

    for f in filters:
        filter_name = f[0]
        filter_value = f[1]

        params[filter_name] = parse_filter_value(filter_value)

    response = s.get(cube_url, params=params, **request_args).json()

    return pd.DataFrame(response)


def parse_filter_value(value: Union[str, List[str]]):
    if type(value) == list:
        return ''.join(value)
    else:
        return value
