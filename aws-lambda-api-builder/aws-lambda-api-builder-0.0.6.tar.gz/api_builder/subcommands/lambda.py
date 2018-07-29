import os
import glob
import shutil
from subprocess import call
import boto3

# valid actions to take
_clean = 'clean'
_build = 'build'
_release = 'release'

# Define the build directories and outputs
_base_dir = os.getcwd()
_build_dir = os.path.join(_base_dir, "build")
_private_dir = os.path.join(_build_dir, "private")
_deps_dir = os.path.join(_private_dir, "deps")
_zip_dir = os.path.join(_private_dir, "lib")
_project_name = os.path.basename(_base_dir)
_output_file = os.path.join(_build_dir, _project_name)


def get_description():
    return 'Package a lambda application and upload to S3'


def set_args(parser):
    action_choices = [_clean, _build, _release]

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

    parser.add_argument("-b", "--bucket")


def execute(args):

    actions = [args.action1, args.action2, args.action3]

    if _clean in actions:
        clean(args)

    if _build in actions:
        build(args)

    if _release in actions:
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
    shutil.make_archive(_output_file, 'zip', _zip_dir)


def release(args):
    print("Uploading to s3")
    if args.bucket is None:
        raise ValueError('You must specify a bucket (--bucket) in order to release')

    s3 = boto3.resource('s3')
    zip_archive = _output_file + '.zip'
    data = open(zip_archive, 'rb')
    s3.Bucket(args.bucket).put_object(Key=os.path.basename(zip_archive), Body=data)


def init_build_dirs():

    if os.path.exists(_zip_dir):
        shutil.rmtree(_zip_dir)

    os.makedirs(_zip_dir, exist_ok=False)
    os.makedirs(_deps_dir, exist_ok=True)

    f = open(os.path.join(_base_dir, '.gitignore'), 'w')
    f.write(os.path.join(_private_dir, '*'))
    f.close()


def copy_source_files():
    python_files = glob.iglob(os.path.join(_base_dir, "*"))
    for file in python_files:

        if file.startswith(_build_dir):
            continue

        if os.path.isdir(file):
            shutil.copytree(file, os.path.join(_zip_dir, os.path.basename(file)))

        if os.path.isfile(file):
            shutil.copy2(file, _zip_dir)


def copy_dep_files():
    # copy pipfiles to deps directory
    shutil.copy2("Pipfile", _deps_dir)
    shutil.copy2("Pipfile.lock", _deps_dir)

    # install dependencies in deps directory
    os.chdir(_deps_dir)
    os.environ["PIPENV_VENV_IN_PROJECT"] = _deps_dir
    call("pipenv install", shell=True)
    os.chdir(_base_dir)

    # move all dependencies to zip directory
    python_files = glob.iglob(os.path.join(_deps_dir, ".venv", "**", "site-packages", "*"), recursive=True)
    for file in python_files:
        print(file)
        target_dir_name = os.path.join(_zip_dir, os.path.basename(file))
        if not os.path.isdir(file):
            continue

        if os.path.exists(target_dir_name):
            shutil.rmtree(target_dir_name)

        shutil.copytree(file, target_dir_name)


if __name__ == "__main__":
    execute(None)