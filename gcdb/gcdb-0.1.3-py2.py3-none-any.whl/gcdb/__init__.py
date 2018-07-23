import os
import sys
import subprocess
import json

import click


@click.command()
@click.argument('command', nargs=-1)
@click.option('--output', default='compile_commands.json', type=click.Path())
def main(command, output):
    os.environ['GCDB'] = os.path.abspath(output)
    gcdb = sys.argv[0]

    cc = os.environ.get('CC', 'cc')
    cxx = os.environ.get('CXX', 'c++')
    os.environ['GCDB_CC'] = cc
    os.environ['GCDB_CXX'] = cxx
    os.environ['CC'] = '{}-cc'.format(gcdb)
    os.environ['CXX'] = '{}-cxx'.format(gcdb)

    with open(output, 'w') as fp:
        json.dump([], fp)

    command = ' '.join(command)
    result = subprocess.run(command, shell=True)
    sys.exit(result.returncode)


def shim():
    # TODO - Assumining that the last arg is path

    command = sys.argv[1:]
    path = command[-1]

    compiler_env = 'GCDB_' + sys.argv[0].rsplit('-', 1)[1].upper()
    compiler = os.environ.get(compiler_env, 'cc')
    print(compiler)

    command = [compiler] + list(command)

    instruction = {
        'directory': os.getcwd(),
        'command': ' '.join(command),
        'file': path,
    }

    subprocess.check_output(' '.join(command), shell=True)

    if path == '-':
        # Configure scripts may output to stdout to test support
        # We don't want to add that to compilation database
        return

    database = os.environ['GCDB']
    if os.path.exists(database):
        with open(database) as fp:
            db = json.load(fp)
    else:
        db = []

    db.append(instruction)

    subprocess.check_output(instruction['command'], shell=True)

    with open(database, 'w') as fp:
        json.dump(db, fp)
