#! /usr/bin/python3

from os import getenv
from subprocess import check_output

from brewblox_tools import deploy_docker, distcopy


def main():
    name = getenv('DOCKER_REPO')

    if not name:
        raise KeyError('Environment variable $DOCKER_REPO not found')

    context = getenv('DOCKER_CONTEXT', 'docker')
    file = getenv('DOCKER_FILE', 'amd/Dockerfile')
    branch = check_output('git rev-parse --abbrev-ref HEAD'.split()).decode().rstrip()

    sdist_result = check_output('python setup.py sdist'.split()).decode()
    print(sdist_result)

    distcopy.main('dist/ docker/dist/'.split())
    distcopy.main('config/ docker/config/'.split())
    deploy_docker.main([
        '--context', context,
        '--file', file,
        '--name', name,
        '--tags', branch,
        '--no-push'
    ])
