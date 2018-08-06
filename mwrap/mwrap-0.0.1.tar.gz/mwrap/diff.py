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

import difflib
import sys
import colorama

def print_unified_diff(diff):
    for d in diff:
        if d.startswith('+++') or d.startswith('---'):
            sys.stdout.write(colorama.Style.BRIGHT)
        elif d.startswith('@@'):
            sys.stdout.write(colorama.Fore.CYAN)
        elif d.startswith('-'):
            sys.stdout.write(colorama.Fore.RED)
        elif d.startswith('+'):
            sys.stdout.write(colorama.Fore.GREEN)
        sys.stdout.write(d + colorama.Style.NORMAL + colorama.Fore.RESET)


def print_wrap_differences(name, wraps):
    if len(wraps) > 1:
        w1, w2 = wraps[0], wraps[1]
        tail = wraps[1:]
        diff = difflib.unified_diff(open(w1, 'r').readlines(), open(w2, 'r').readlines(), fromfile=w1, tofile=w2)
        print_unified_diff(diff)
        print_wrap_differences(name, tail)


