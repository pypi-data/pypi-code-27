
import os

from subprocess import call

from api_builder import configuration
from api_builder import cloudformation

_cf_bootstrap = "bootstrap.yml"
_cf_lambda = "lambda.yml"
_cf_api = "api.yml"
_py_endpoint = "endpoint.py"


def get_description():
    return 'Bootstrap a Lambda API'


def set_args(parser):
    # todo: make non optional
    parser.add_argument("-n", "--name")


def execute(args):

    if os.path.exists("zlab-conf.json"):
        raise ValueError("Application has already been bootstrapped. Delete 'zlab-conf.json' to unbootstrap")

    print("Initializing project structure")
    os.makedirs(configuration._cf_dir, exist_ok=True)
    write_file(_cf_bootstrap, configuration._cf_dir)
    write_file(_cf_lambda, configuration._cf_dir)
    write_file(_cf_api, configuration._cf_dir)
    write_file(_py_endpoint, configuration._base_dir)

    print("Initializing pipenv")
    call("pipenv install", shell=True)

    print("Writing configuration file")
    conf = {
        "api_name": args.name
    }
    configuration.write_zlab_conf(conf)

    print("Updating bootstrap stack")
    conf['s3_bucket_name'] = 'zlab-' + conf["api_name"].lower() + '-lambda-code'
    configuration.write_zlab_conf(conf)
    cloudformation.main(conf["api_name"] + "-bootstrap", "cloudformation\\bootstrap.yml", conf)

def write_file(file, dir):
    in_path = os.path.join(configuration.STATIC_DIR, file)
    out_path = os.path.join(dir, file)
    if not os.path.exists(out_path):
        with open(in_path) as output:
            f = open(out_path, 'w')
            f.write(output.read())
            f.close()