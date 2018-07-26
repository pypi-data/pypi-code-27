import argparse
import ecs_auditor
from ecs_auditor.client import Client
import ecs_auditor.config as config

def execute():
    """Entry point for the application script"""
    parser = argparse.ArgumentParser(description='Command line arguments')
    parser.add_argument('--region', metavar='[region]', default='all', help='AWS region to get data for? [default: all, options: [us-east-1, eu-central-1, eu-west-1, all] ]')
    parser.add_argument('--env', metavar='[env]', default='all', help='AWS environment to get data for? [default: all, options: [preprod, prod, all] ]')
    parser.add_argument('--output', metavar='[output]', default='pretty', help='How to display the results. [default: pretty, options: [pretty, json, compare] ]')
    parser.add_argument('--ignore-author', metavar='[ignore-author]', default='', help='Results exludung specific param author. [default: None, options: string')
    parser.add_argument('--services', metavar='[services]', default='', help='Specify a single service. [default: None, options: string')
    parser.add_argument('--show-differences-only', default=False, type=lambda x: (str(x).lower() == 'true'))
    parser.add_argument('--config', help='Specify location of the config file')
    args = parser.parse_args()
    config.settings = config.load_config(args.config)

    Client(args.config, args.region.lower(), args.output.lower(), args.env.lower(), args.services.lower(), args.ignore_author.lower(), args.show_differences_only).perform()

if __name__ == '__main__':
    execute()
