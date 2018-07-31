import argparse
import eip_auditor
from eip_auditor.client import Client

def execute():
    """Entry point for the application script"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", help="selected region to perform the scan")
    parser.add_argument("--ip_addresses", help="the cidr block to search for in the security groups")
    args = parser.parse_args()
    if args is None:
        raise "Args not set"

    if args.region is None and args.ip_addresses is not None:
        raise "Error: --ip_addresses is specified, but --region was not."

    Client(args.region, args.ip_addresses).perform()

if __name__ == '__main__':
    execute()
