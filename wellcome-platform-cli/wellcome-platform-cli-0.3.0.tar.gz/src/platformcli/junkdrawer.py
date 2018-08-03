# -*- encoding: utf-8
"""
A miscellaneous collection of functions and helpers for use in the CLI.
Named junkdrawer.py because I haven't prganised it properly.

https://twitter.com/betsythemuffin/status/1003313844108824584

"""

import os
import re
import sys

from .superprocess import check_call, check_output


ROOT = check_output('git', 'rev-parse', '--show-toplevel')

RELEASE_FILE = os.path.join(ROOT, 'RELEASE.md')

MAJOR = 'major'
MINOR = 'minor'
PATCH = 'patch'

VALID_RELEASE_TYPES = (MAJOR, MINOR, PATCH)

RELEASE_TYPE = re.compile(r"^RELEASE_TYPE: +(%s|%s|%s)" % VALID_RELEASE_TYPES)


def git(*args):
    check_call('git', *args)


def get_changed_paths(*args):
    """
    Returns a set of changed paths in a given commit range.

    :param commit_range: Arguments to pass to ``git diff``.
    """
    diff_output = check_output('git', 'diff', '--name-only', *args)

    return set([
        line.strip()
        for line in diff_output.splitlines()
    ])


def run_formatting(run_all=False):
    """
    Run all the formatting scripts.
    """
    if not run_all:
        changed_paths = get_changed_paths('HEAD', 'master')

    if run_all or any(f.endswith(('.sbt', '.scala')) for f in changed_paths):
        check_call('sbt', 'scalafmt')

    if run_all or any(f.endswith('.tf') for f in changed_paths):
        check_call('terraform', 'fmt')


def tags():
    """
    Returns a list of all tags in the repo.
    """
    git('fetch', '--tags')
    result = check_output('git', 'tag')
    all_tags = result.split('\n')

    assert len(set(all_tags)) == len(all_tags)

    return set(all_tags)


def latest_version():
    """
    Returns the latest version, as specified by the Git tags.
    """
    versions = []

    all_tags = tags()

    for t in all_tags:
        assert t == t.strip()
        parts = t.split('.')
        assert len(parts) == 3, t
        parts[0] = parts[0].lstrip('v')
        v = tuple(map(int, parts))

        versions.append((v, t))

    _, latest = max(versions)

    assert latest in all_tags
    return latest


def modified_files():
    """
    Returns a list of all files which have been modified between now
    and the latest release.
    """
    files = set()
    for command in [
        ('git', 'diff', '--name-only', '--diff-filter=d',
            latest_version(), 'HEAD'),
        ('git', 'diff', '--name-only')
    ]:
        diff_output = check_output(*command)
        for l in diff_output.split('\n'):
            filepath = l.strip()
            if filepath:
                assert os.path.exists(filepath)
                files.add(filepath)
    return files


def has_source_changes():
    """
    Returns True if there are source changes since the previous release,
    False if not.
    """
    changed_files = [
        f for f in modified_files() if f.strip().endswith(('.sbt', '.scala'))
    ]
    return len(changed_files) != 0


def has_release():
    """
    Returns True if there is a release file, False if not.
    """
    return os.path.exists(RELEASE_FILE)


def parse_release_file():
    """
    Parses the release file, returning a tuple (release_type, release_contents)
    """
    with open(RELEASE_FILE) as i:
        release_contents = i.read()

    release_lines = release_contents.split('\n')

    m = RELEASE_TYPE.match(release_lines[0])
    if m is not None:
        release_type = m.group(1)
        if release_type not in VALID_RELEASE_TYPES:
            print('Unrecognised release type %r' % (release_type,))
            sys.exit(1)
        del release_lines[0]
        release_contents = '\n'.join(release_lines).strip()
    else:
        print(
            'RELEASE.md does not start by specifying release type. The first '
            'line of the file should be RELEASE_TYPE: followed by one of '
            'major, minor, or patch, to specify the type of release that '
            'this is (i.e. which version number to increment). Instead the '
            'first line was %r' % (release_lines[0],)
        )
        sys.exit(1)

    return release_type, release_contents
