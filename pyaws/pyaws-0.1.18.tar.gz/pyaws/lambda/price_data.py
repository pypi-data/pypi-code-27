"""
Retrieve Amazon Web Services Pricing
"""
import json
import requests

INDEXURL = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json"
url_prefix = "https://pricing.us-east-1.amazonaws.com"


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


def price_data(service, region, sku=None):
    """
    Summary:
        all price data for an AWS service
    Return:
        data (json)
    """
    r = requests.get(region_index(service, region))
    if sku:
        return json.loads(r.content)['products'][sku]
    return json.loads(r.content)['products']


price_data("AWSLambda", 'eu-west-1')    
