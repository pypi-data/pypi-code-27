# Copyright 2018 Daniel Zalevskiy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-

import os
import sys
from collections import defaultdict
import pygit2
import colorama

from .find import find_wraps_recursive
from .find import find_wrap
from .find import find_wraps
from .diff import print_wrap_differences
from .parse import extract_value_from_wrap
from .parse import parse_wrap

colorama.init()


def diff_wrap(args):
    wraps = find_wraps_recursive()
    wrap_map = defaultdict(list)

    for wrap in wraps:
        name = os.path.splitext(os.path.basename(wrap))[0]
        if (args.name is not None) and (name != args.name):
            continue
        wrap_map[name] += [wrap]

    if (args.name is not None) and len(wrap_map) == 0:
        print('No wrap with name', args.name)
        return 1

    for name, wrap_list in wrap_map.items():
        print_wrap_differences(name, wrap_list)
    return 0


def _print_status(wrap_name, color_prefix, msg):
    sys.stdout.write(colorama.Style.BRIGHT + wrap_name + ": ")
    sys.stdout.write(colorama.Style.RESET_ALL)
    sys.stdout.write(color_prefix + msg + os.linesep)
    sys.stdout.write(colorama.Style.RESET_ALL)
    sys.stdout.flush()


def _print_status_ok(wrap_name, msg='ok'):
    _print_status(wrap_name, colorama.Fore.GREEN, msg)


def _print_status_not_ok(wrap_name, msg):
    _print_status(wrap_name, colorama.Fore.RED, msg)


def _wrap_status(wrap):
    pass


def status(args):
    wrap_file_paths = []
    if args.name is not None:
        wrap_path = find_wrap(args.name)
        if wrap_path is None:
            print('No wrap with name', args.name)
            return 1
        wrap_file_paths = [wrap_path]
    else:
        wrap_file_paths = find_wraps()
    for wrap_path in wrap_file_paths:
        try:
            wrap = parse_wrap(wrap_path)
        except Exception as e:
            print("failed to parse file '{}': {}".format(wrap_path, e))
            return 1
        wrap_name = wrap_path[:-5]
        dir_path = os.path.join('subprojects', wrap.directory)
        if not os.path.exists(dir_path):
            _print_status_not_ok(wrap_name, "directory missing")
            continue
        if wrap.wrap_type == 'wrap-git':
            try:
                repo = pygit2.Repository(dir_path)
            except Exception as e:
                _print_status_not_ok(wrap_name, 'invalid git repository')
                continue

            status_msgs = []
            for status in repo.status().values():
                if status != pygit2.GIT_STATUS_IGNORED:
                    status_msgs.append('modified')
                    break

            #if repo.head_is_detached:
            #    status_msgs.append('detached')

            rev = repo.head.target.hex
            if wrap.revision.lower() == 'head':
                head_hash = repo.branches.get('origin/HEAD').get_object().id.hex
                if rev != head_hash:
                    status_msgs.append('not up to date with origin')
            else:
                branch = repo.branches.get(wrap.revision)
                if branch is not None:
                    if branch.get_object().hex != repo.branches.get('origin/' + wrap.revision).get_object().hex:
                        status_msgs.append('not up to date with origin')
                else:
                    try:
                        commit = repo.revparse_single(wrap.revision)
                        if commit.hex != repo.head.target.hex:
                            status_msgs.append('revision mismatch')
                    except:
                        status_msgs.append('invalid revision')

            if len(status_msgs) == 0:
                _print_status_ok(wrap_name)
            else:
                _print_status_not_ok(wrap_name, ', '.join(status_msgs))
        else:
            if args.name is not None:
                print("wrap '{}' is not of kind 'wrap-git'".format(args.name))
                return 1
            else:
                _print_status_ok(wrap_name)

