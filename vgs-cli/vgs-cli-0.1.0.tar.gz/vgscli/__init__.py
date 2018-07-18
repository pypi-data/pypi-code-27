from vgscli.routes import dump_all_routes, sync_all_routes, create_all_routes
from vgscli.utils import is_file_accessible, eprint

__version__ = '0.1.0'

import yaml
import sys
import getpass
import tempfile
import os

from vgscli.auth import login, valid_expiration, get_config_path
from simple_rest_client.api import API
from simple_rest_client.resource import Resource


class RouteResource(Resource):
    actions = {
        'retrieve': {'method': 'GET', 'url': 'rule-chains/{}'},
        'create': {'method': 'POST', 'url': 'rule-chains'},
        'list': {'method': 'GET', 'url': 'rule-chains'},
        'delete': {'method': 'DELETE', 'url': 'rule-chains/{}'},
        'update': {'method': 'PUT', 'url': 'rule-chains/{}'},
    }


def create_api(tenant, environment, token, tld):
    if environment and not environment.endswith('.'):
        environment += '.'
    api = API(
        api_root_url='https://api.{environment}{tld}'.format(
            environment=environment,
            tld=tld,
        ),
        params={},  # default params
        headers={
            'VGS-Tenant': tenant,
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json',
            'User-Agent': 'VGS CLI {}'.format(__version__),
            'Authorization': 'Bearer {}'.format(token)
        },  # default headers
        timeout=50,  # default timeout in seconds
        append_slash=False,  # append slash to final url
        json_encode_body=True,  # encode body as json
    )
    api.add_resource(resource_name='routes', resource_class=RouteResource)
    return api


def check_auth(config):
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, 'vgs_token')

    if is_file_accessible(temp_file, 'r+'):
        with open(temp_file, 'r+') as tmp:
            existing_token = tmp.read()

            if existing_token and valid_expiration(existing_token):
                return existing_token

    eprint('Enter your username: ')
    try:
        username = input('')
    except EOFError:
        eprint("Please use \"vgs authenticate\" before providing input file stream")
        sys.exit(1)

    password = getpass.getpass('Enter your password: ')
    access_token = login(config, username, password)

    with open(temp_file, 'w+') as tmp:
        tmp.write(access_token)

    return access_token


def load_config():
    config_path = get_config_path()
    try:
        with open(config_path, 'r') as stream:
            return yaml.load(stream)
    except (yaml.YAMLError, OSError) as exc:
        eprint("Can not find or process config file: " + config_path)
        eprint(exc)
        sys.exit(1)


def main(args):
    config = load_config()
    token = check_auth(config)
    if args.subparser_name == 'authenticate':
        # don't need to do anything, just process the auth
        pass

    if args.subparser_name == 'route':
        if not args.tenant:
            eprint("Please specify --tenant option.")

        api = create_api(args.tenant, args.environment, token, args.tld)
        if args.dump_all:
            dump_all_routes(api)
        if args.sync_all:
            sync_all_routes(api, args.tenant)
        if args.create_all:
            create_all_routes(api, args.tenant)
