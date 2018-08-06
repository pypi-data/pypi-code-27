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

import argparse
import colorama

from . import commands

def main():
    colorama.init()

    parser = argparse.ArgumentParser(description='Meson subproject tool', prog='mwrap')
    subparsers = parser.add_subparsers(title='Commands', dest='command')
    subparsers.required = True #kwarg doesn't work

    p = subparsers.add_parser('diff-wrap', help='Show wrap file differences between subproject and subsubproject')
    p.add_argument('name', help='subproject name', nargs='?')
    p.set_defaults(command=commands.diff_wrap)

    p = subparsers.add_parser('status', help='Show subproject status')
    p.add_argument('name', help='subproject name', nargs='?')
    p.set_defaults(command=commands.status)

    args = parser.parse_args()
    return args.command(args)

