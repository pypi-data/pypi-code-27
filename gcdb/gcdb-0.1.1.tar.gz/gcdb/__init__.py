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
    os.environ['CC'] = '{} -- {}'.format(gcdb, cc)
    os.environ['CXX'] = '{} -- {}'.format(gcdb, cxx)

    command = ' '.join(command)
    result = subprocess.run(command, shell=True)
    sys.exit(result.returncode)


@click.command()
@click.argument('command', nargs=-1)
def inner(command):
    # TODO - Assumining that the last arg is path
    path = command[-1]

    instruction = {
        'directory': os.getcwd(),
        'command': ' '.join(command),
        'file': path,
    }

    subprocess.check_output(' '.join(command), shell=True)

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


if 'GCDB' in os.environ:
    cli = inner
else:
    cli = main
