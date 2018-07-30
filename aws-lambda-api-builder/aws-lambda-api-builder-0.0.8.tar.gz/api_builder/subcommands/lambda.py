import os
import glob
import shutil
from subprocess import call
import boto3
from api_builder import cloudformation
from api_builder import configuration
import time

# valid actions to take
_clean = 'clean'
_build = 'build'
_deploy = 'deploy'

# Define the build directories and outputs
_output_file = os.path.join(configuration._build_dir, configuration._project_name + "." + str(time.time()))


def get_description():
    return 'Package a lambda application and upload to S3'


def set_args(parser):
    action_choices = [_clean, _build, _deploy]

    parser.add_argument(
        'action1',
        choices=action_choices,
        nargs="?")

    parser.add_argument(
        'action2',
        choices=action_choices,
        nargs="?")

    parser.add_argument(
        'action3',
        choices=action_choices,
        nargs="?")


def execute(args):

    actions = [args.action1, args.action2, args.action3]

    if _clean in actions:
        clean(args)

    if _build in actions:
        #todo: delete any old built .zip files
        build(args)

    if _deploy in actions:
        release(args)


def clean(args):
    base_dir = os.getcwd()
    build_dir = os.path.join(base_dir, "build")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)


def build(args):
    init_build_dirs()
    copy_source_files()
    copy_dep_files()

    conf = configuration.get_zlab_conf()
    conf["s3_bucket_key"] = os.path.basename(_output_file + '.zip')
    configuration.write_zlab_conf(conf)
    shutil.make_archive(_output_file, 'zip', configuration._zip_dir)


def release(args):
    configuration.check_bootstrap()
    conf = configuration.get_zlab_conf()
    zip_archive = os.path.join(configuration._build_dir, conf["s3_bucket_key"])
    print("Uploading " + zip_archive + " to bucket " + conf['s3_bucket_name'])
    s3 = boto3.resource('s3')

    #todo: check if file exists, if it does then no reason to delete
    data = open(zip_archive, 'rb')
    s3.Bucket(conf["s3_bucket_name"]).put_object(Key=conf["s3_bucket_key"], Body=data)

    print("Updating lambda stack")
    cf_path = os.path.join(configuration._cf_dir, "lambda.yml")
    cloudformation.main(conf["api_name"] + "-lambda", cf_path, conf)

def init_build_dirs():

    if os.path.exists(configuration._zip_dir):
        shutil.rmtree(configuration._zip_dir)

    os.makedirs(configuration._zip_dir, exist_ok=False)
    os.makedirs(configuration._deps_dir, exist_ok=True)


def copy_source_files():
    python_files = glob.iglob(os.path.join(configuration._base_dir, "*"))
    for file in python_files:

        if file.startswith(configuration._build_dir):
            continue

        if os.path.isdir(file):
            shutil.copytree(file, os.path.join(configuration._zip_dir, os.path.basename(file)))

        if os.path.isfile(file):
            shutil.copy2(file, configuration._zip_dir)


def copy_dep_files():
    # copy pipfiles to deps directory
    shutil.copy2("Pipfile", configuration._deps_dir)
    shutil.copy2("Pipfile.lock", configuration._deps_dir)

    # install dependencies in deps directory
    os.chdir(configuration._deps_dir)
    os.environ["PIPENV_VENV_IN_PROJECT"] = configuration._deps_dir
    call("pipenv install", shell=True)
    os.chdir(configuration._base_dir)

    # move all dependencies to zip directory
    python_files = glob.iglob(os.path.join(configuration._deps_dir, ".venv", "**", "site-packages", "*"), recursive=True)
    for file in python_files:
        print(file)
        target_dir_name = os.path.join(configuration._zip_dir, os.path.basename(file))
        if not os.path.isdir(file):
            continue

        if os.path.exists(target_dir_name):
            shutil.rmtree(target_dir_name)

        shutil.copytree(file, target_dir_name)


if __name__ == "__main__":
    execute(None)