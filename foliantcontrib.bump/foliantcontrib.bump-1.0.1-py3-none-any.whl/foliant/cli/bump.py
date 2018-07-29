'''Version bumper for Foliant projects.'''

import re
from pathlib import Path

from semver import bump_major, bump_minor, bump_patch, bump_prerelease, bump_build
from cliar import set_help, set_arg_map

from foliant.cli.base import BaseCli


class Cli(BaseCli):
    @set_arg_map({'project_path': 'path', 'config_file_name': 'config'})
    @set_help(
        {
            'version_part': 'Part of the version to bump: '
                            + 'major, minor, patch, prerelease, or build '
                            + '(default: patch).',
            'project_path': 'Path to the directory with the config file (default: ".").',
            'config_file_name': 'Name of the config file (default: "foliant.yml").'
        }
    )
    def bump(self, version_part='patch', project_path=Path('.'), config_file_name='foliant.yml'):
        '''Bump Foliant project version.'''

        try:
            bump_function = {
                'major': bump_major,
                'minor': bump_minor,
                'patch': bump_patch,
                'prerelease': bump_prerelease,
                'build': bump_build
            }[version_part]

        except KeyError as exception:
            quit(f'Unknown version part {exception}.')

        version_line_pattern = re.compile(r'^(version:\s*)(?P<version>.+)$', flags=re.MULTILINE)

        try:
            with open(project_path/config_file_name, encoding='utf8') as config_file:
                config = config_file.read()

        except FileNotFoundError:
            quit(f'No config file named {config_file_name} found in "{project_path}".')

        version_line = version_line_pattern.search(config)

        if not version_line:
            quit('No version defined in the config file.')

        old_version = version_line.group('version')

        new_version = bump_function(old_version)

        with open(project_path/config_file_name, 'w', encoding='utf8') as config_file:
            config_file.write(version_line_pattern.sub(rf'\g<1>{new_version}', config))

        self.logger.info('Version bumping completed.')

        print(f'Bumped version from {old_version} to {new_version}.')
