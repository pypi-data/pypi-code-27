__version__ = '0.0.1'

import yaml
import sys
import getpass
import tempfile
import os

from vgscli.auth import login, valid_expiration, get_config_path
from simple_rest_client.api import API
from simple_rest_client.resource import Resource


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class RouteResource(Resource):
    actions = {
        'retrieve': {'method': 'GET', 'url': 'rule-chains/{}'},
        'create': {'method': 'POST', 'url': 'rule-chains'},
        'list': {'method': 'GET', 'url': 'rule-chains'},
        'delete': {'method': 'DELETE', 'url': 'rule-chains/{}'},
        'update': {'method': 'PUT', 'url': 'rule-chains/{}'},
    }


def create_api(tenant, environment, token):
    api = API(
        api_root_url='https://api.{}.verygoodsecurity.com'.format(environment),
        params={}, # default params
        headers={
            'VGS-Tenant': tenant,
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json',
            'User-Agent': 'VGS CLI {}'.format(__version__),
            'Authorization': 'Bearer {}'.format(token)
        }, # default headers
        timeout=50, # default timeout in seconds
        append_slash=False, # append slash to final url
        json_encode_body=True, # encode body as json
    )
    api.add_resource(resource_name='routes', resource_class=RouteResource)
    return api


def map_routes(data):
    return data


def dump_all_routes(api):
    result = api.routes.list()
    body = result.body

    updated = {
        'version': 1,
        'data': map_routes(body['data']),
    }

    print(yaml.dump(updated))


def sync_all_routes(api):
    config = sys.stdin.read()
    # print(config)
    payloads = yaml.load(config)
    results = []
    for route in payloads['data']:
        route_id = route['id']
        # print(route)
        payload = {'data': route}
        result = api.routes.update(route_id, body=payload)
        body = result.body
        # print(result)
        # print result.body
        results.append(result.body['data'])

    updated = {
        'version': 1,
        'data': results,
    }
    # print([item['id'] for item in payload['data']])
    #
    # body = result.body
    # # print(json.dumps(body, indent=2))
    print(yaml.dump(updated))


def check_auth(config):
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, 'vgs_token')

    if os.path.exists(temp_file):
        with open(temp_file, 'r+') as tmp:
            existing_token = tmp.read()

            if existing_token and valid_expiration(existing_token):
                return existing_token

    eprint('Enter your username: ')
    username = input('')
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
    # eprint(args)

    config = load_config()
    token = check_auth(config)

    if args.subparser_name == 'route':
        api = create_api(args.tenant, args.environment, token)
        if args.dump_all:
            dump_all_routes(api)
        if args.sync_all:
            sync_all_routes(api)
