import yaml
import sys

from vgscli.utils import eprint


def dump_all_routes(api):
    result = api.routes.list()
    body = result.body

    updated = {
        'version': 1,
        'data': body['data'],
    }

    dump = yaml.dump(updated)

    print(dump)


def sync_all_routes(api, tenant):
    __write_routes(tenant, lambda route_id, payload: api.routes.update(route_id, body=payload))


def create_all_routes(api, tenant):
    __write_routes(tenant, lambda route_id, payload: api.routes.create(route_id, body=payload))


def __write_routes(tenant, api_call_function):
    config = sys.stdin.read()

    payloads = yaml.load(config)
    results = []
    for route in payloads['data']:
        route_id = route['id']
        payload = {'data': route}
        result = api_call_function(route_id, payload)
        eprint('Route {} processed'.format(route_id))
        results.append(result.body['data'])

    updated = {
        'version': 1,
        'data': results,
    }

    print(yaml.dump(updated))
    eprint("Routes written successfully for tenant " + tenant)
