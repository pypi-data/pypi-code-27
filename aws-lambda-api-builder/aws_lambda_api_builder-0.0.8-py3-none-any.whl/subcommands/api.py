from api_builder import cloudformation
from api_builder import configuration
import os

_deploy = 'deploy'

def get_description():
    return 'Bootstrap a Lambda API'


def set_args(parser):
    action_choices = [_deploy]

    parser.add_argument(
        'action1',
        choices=action_choices,
        nargs="?")


def execute(args):
    configuration.check_bootstrap()

    actions = [args.action1]
    if _deploy in actions:
        print("Updating apigateway stack")
        conf = configuration.get_zlab_conf()
        cf_path = os.path.join(configuration._cf_dir, "api.yml")
        cloudformation.main(conf["api_name"] + "-api", cf_path, conf)

