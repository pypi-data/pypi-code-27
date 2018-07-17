"""
    Global namespace for gmq.commands.
"""
# pylint: disable=C0103,C0325

import docopt

def build_api_opts_from_docopt_args(args):
    api_opts = {}
    _ = api_opts.update(
        {'debug': args.get('--debug')})
    _ = api_opts.update(
        {'murano_id': args.get('--uuid')})
    _ = api_opts.update(
        {'murano_token': args.get('--token')})
    _ = api_opts.update(
        {'http_timeout': args.get('--timeout')})
    _ = api_opts.update(
        {'murano_host': args.get('--host')})
    _ = api_opts.update(
        {'murano_port': args.get('--port')})
    _ = api_opts.update(
        {'certfile': args.get('--cert'),
         'pkeyfile': args.get('--pkey')})
    _ = api_opts.update({'murano_cacert': args.get('--cacert')})
    return api_opts

# TODO: The Command class in both http and mqtt are 99% the same.
#       The classes should be broken out, generalized and abstracted
#       here so they may be either subclassed or monkey patched in
#       their respective command __init__ files.