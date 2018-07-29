"""
Retrieve Amazon Web Services Pricing
"""
import argparse
import os
import sys
import json
import logging
import inspect
import requests
from functools import lru_cache
from itertools import chain
from pygments import highlight, lexers, formatters
import boto3


# globals
PROFILE = 'default'
__version__ = '1.0 '
logger = logging.getLogger(__version__)
logger.setLevel(logging.INFO)

# set region default
default_region = os.getenv('AWS_DEFAULT_REGION', 'eu-west-1')
default_region = 'eu-west-1'

RETURN_DATA = ['compute', 'transfer', 'request', 'requests', 'edge']
INDEXURL = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json"
url_prefix = "https://pricing.us-east-1.amazonaws.com"


def export_json_object(dict_obj, filename=None):
    """
    Summary:
        exports object to block filesystem object

    Args:
        :dict_obj (dict): dictionary object
        :filename (str):  name of file to be exported (optional)

    Returns:
        True | False Boolean export status

    """
    try:
        if filename:
            try:
                with open(filename, 'w') as handle:
                    handle.write(json.dumps(dict_obj, indent=4, sort_keys=True))
                    logger.info(
                        '%s: Wrote %s to local filesystem location' %
                        (inspect.stack()[0][3], filename))
                handle.close()
            except TypeError as e:
                logger.warning(
                    '%s: object in dict not serializable: %s' %
                    (inspect.stack()[0][3], str(e)))
        else:
            json_str = json.dumps(dict_obj, indent=4, sort_keys=True)
            print(highlight(json_str, lexers.JsonLexer(), formatters.TerminalFormatter()))
            logger.info('%s: successful export to stdout' % inspect.stack()[0][3])
            return True
    except OSError as e:
        logger.critical(
            '%s: export_file_object: error writing to %s to filesystem. Error: %s' %
            (inspect.stack()[0][3], filename, str(e)))
        return False
    else:
        logger.info('export_file_object: successful export to %s' % filename)
        return True


def get_regions(name):
    session = boto3.Session(profile_name=name)
    ec2 = session.client('ec2', region_name=default_region)
    return [x['RegionName'] for x in ec2.describe_regions()['Regions'] if 'cn' not in x['RegionName']]


def global_index(service, url=INDEXURL):
    """
    Retrieves master index file containing current price file urls for all AWS Services
    """
    r = requests.get(INDEXURL)
    f1 = json.loads(r.content)
    return url_prefix + f1['offers'][service]['currentRegionIndexUrl']


def region_index(region):
    """
    Returns url of price file for specific region
    """
    r2 = requests.get(global_index(service='AWSLambda'))
    return url_prefix + json.loads(r2.content)['regions'][region]['currentVersionUrl']


@lru_cache()
def price_data(region, sku=None):
    """
    Summary:
        all price data for an AWS service
    Return:
        data (json)
    """
    r = requests.get(region_index(region)).json()

    products = [x for x in r['products'].values() if x['attributes']['servicecode'] == 'AWSLambda']
    skus = {x['sku'] for x in products}

    terms = list(chain(
        *[
            y.values() for y in [x for x in r['terms'].values()]
        ]
    ))

    parsed = []

    for term in terms:
        if list(term.values())[0]['sku'] not in skus:
            continue
        parsed.append(term)
    return products, skus, parsed


def help_menu():
    """ Displays command line parameter options """
    menu = '''
                        help menu
                        ---------

DESCRIPTION

        Code returns AWS Price data metrics for AWS Lambda

OPTIONS

        $ python3 get_price.py  [OPTIONS]

                [-e, --element   <value> ]
                [-f, --filename  <value> ]
                [-r, --region   <value> ]
                [-d, --debug     ]
                [-h, --help      ]

        -e, --element (string):  Data Return Type.  Data element
            returned when one of the following specified:

                - compute  :  AWS Lambda Compute Price ($/GB-s)
                - transfer :  AWS Lambda Bandwidth Price ($/GB)
                - request  :  Price per request ($/req)
                - edge     :  Compute Price Lambda Edge ($/GB-s)

        If no --element specified, the entire pricing json object
        for the region returned

        -f, --filename (string):  Name of output file. Valid when
            a data element is NOT specified and you want the entire
            pricing json object returned and persisted to the
            filesystem.  No effect when --element given.

        -r, --region (string):  Region for which you want to return
            pricing.  If no region parameter specified, defaults to
            eu-west-1

        -d, --debug: Debug mode, verbose output.

        -h, --help: Print this menu
    '''
    print(menu)
    return True


def main(region, dataType=None, output_path=None):
    products, skus, response = price_data(region=region)
    if dataType and dataType == 'compute':
        for k,v in response[4]['SGGKTWDV7PGMPPSJ.JRTCKXETXF']['priceDimensions'].items():
            if isinstance(v, dict):
                for key, value in v.items():
                    if key == 'pricePerUnit':
                        return value['USD']
    elif dataType and dataType == 'transfer':
        for k,v in response[1]['B5V2RNHAWGVJBZD3.JRTCKXETXF']['priceDimensions'].items():
            if isinstance(v, dict):
                for key, value in v.items():
                    if key == 'pricePerUnit':
                        return value['USD']
    elif dataType and dataType in ('request', 'requests'):
        for k,v in response[0]['DDKXA6JP8NCVUFRZ.JRTCKXETXF']['priceDimensions'].items():
            if isinstance(v, dict):
                for key, value in v.items():
                    if key == 'pricePerUnit':
                        return value['USD']
    elif dataType and dataType == 'edge':
        for k,v in response[-1]['WUTD23YJE55E5JCC.JRTCKXETXF']['priceDimensions'].items():
            if isinstance(v, dict):
                for key, value in v.items():
                    if key == 'pricePerUnit':
                        return value['USD']
    return export_json_object(dict_obj=response, filename=output_path)


def options(parser, help_menu=False):
    """
    Summary:
        parse cli parameter options
    Returns:
        TYPE: argparse object, parser argument set
    """
    parser.add_argument("-e", "--element", nargs='?', default='list', type=str,
                        choices=RETURN_DATA, required=False)
    parser.add_argument("-f", "--filename", nargs='?', default=None,
                              required=False, help="type (default: %(default)s)")
    parser.add_argument("-r", "--region", nargs='?', default=default_region, type=str,
                        choices=get_regions(PROFILE), required=False)
    parser.add_argument("-d", "--debug", dest='debug', action='store_true', required=False)
    parser.add_argument("-h", "--help", dest='help', action='store_true', required=False)
    return parser.parse_args()


def init_cli():
    # parser = argparse.ArgumentParser(add_help=False, usage=help_menu())
    parser = argparse.ArgumentParser(add_help=False)

    try:
        args = options(parser)
    except Exception as e:
        logger.exception('Problem parsing provided parameters: %s' % str(e))
    if args.help:
        return help_menu()
    if args.debug:
        print('\n\nParameters:\n\targs.region:\t%s\n\targs.element:\t%s\n' % (args.region, args.element))
    return main(region=args.region, dataType=args.element, output_path=args.filename)


if __name__ == '__main__':
    sys.exit(init_cli())
