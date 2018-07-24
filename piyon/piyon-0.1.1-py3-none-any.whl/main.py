import argparse
import os
import shutil


def run():
    args = parseArgs()
    projectName = args.projectName
    if os.path.exists(projectName):
        shutil.rmtree(projectName)
        # raise SyntaxError('dir {} already exists'.format(projectName))
    source_dir = os.path.dirname(__file__) + os.sep + 'template'
    tmp_dir = os.getcwd() + os.sep + 'tmp'
    try:
        shutil.copytree(source_dir, tmp_dir, ignore=ignore_pyc_files)

        setup_py = tmp_dir + os.sep + 'setup.py'

        with open(setup_py, 'rt') as f:
            data = f.read()

        replacedData = data.replace('$PROJECT_NAME$', projectName)

        with open(setup_py, 'wt') as f:
            f.write(replacedData)

        shutil.move('tmp', projectName)
    except Exception:
        if os.path.exists('tmp'):
            shutil.rmtree('tmp')


def parseArgs():
    parser = argparse.ArgumentParser(description='create a pytest project')

    parser.add_argument(dest='projectName', metavar='project_name')

    args = parser.parse_args()

    return args


def ignore_pyc_files(dirname, filenames):
    return [name for name in filenames if name.endswith('.pyc') or name == '__pycache__']
