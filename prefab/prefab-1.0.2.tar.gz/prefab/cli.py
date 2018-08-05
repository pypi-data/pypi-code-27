import argparse
import subprocess

from prefab import templating
from prefab.filesystem import mkdirp


def main() -> None:
    project_name = parse_args().project_name
    scaffold_project(project_name)
    scaffold_pipenv(project_name)
    commit(project_name)
    print_help(project_name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('project_name')
    return parser.parse_args()


def scaffold_project(project_name: str) -> None:
    # Repository root directory.
    mkdirp(project_name)
    context = {
        'project_name': project_name,
    }
    templating.ensure(
        source='setup.py',
        destination=f'{project_name}/setup.py',
        context=context,
    )

    # Application directory.
    mkdirp(f'{project_name}/{project_name}')
    templating.ensure(
        source='main.py',
        destination=f'{project_name}/{project_name}/main.py',
    )

    # Tests directory.
    mkdirp(f'{project_name}/tests')
    templating.ensure(
        source='test_main.py',
        destination=f'{project_name}/tests/test_main.py',
        context=context,
    )


def scaffold_pipenv(project_name: str) -> None:
    subprocess.check_call(
        [
            'pipenv',
            'install',
            '-e',
            '.',
        ],
        cwd=project_name,
    )
    subprocess.check_call(
        [
            'pipenv',
            'install',
            '--dev',
            'pytest',
        ],
        cwd=project_name,
    )


def commit(project_name: str) -> None:
    subprocess.check_call(
        [
            'git',
            'init',
        ],
        cwd=project_name,
    )
    subprocess.check_call(
        [
            'git',
            'add',
            '.',
        ],
        cwd=project_name,
    )
    staged_changes = subprocess.check_output(
        [
            'git',
            'diff',
            '--staged',
        ],
        cwd=project_name,
    )
    if not staged_changes:
        return

    subprocess.check_call(
        [
            'git',
            'commit',
            '--message',
            'Initial commit',
        ],
        cwd=project_name,
    )


def print_help(project_name: str) -> None:
    print()
    print(f'✨✨ {project_name} successfully prefabricated! ✨✨')
    print()
    print('To get started, run:')
    print()
    print(f'    cd {project_name} && pipenv run pytest tests')
    print()
