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


class Wrap:
    wrap_type = ''

    def __getitem__(self, key):
        return self.values[key]


def parse_wrap(wrap_path):
    f = open(wrap_path, 'r')
    header = f.readline().strip()
    line_num = 1
    if len(header) < 3 or header[0] != '[' or header[-1] != ']':
        raise SyntaxError("invalid wrap header '{}'".format(header))
    kind = header[1:-1]
    if kind != 'wrap-git' and kind != 'wrap-file':
        raise SyntaxError("invalid wrap kind '{}'".format(kind))

    wrap = Wrap()
    wrap.wrap_type = kind
    values = dict()
    for line in f.readlines():
        line_num += 1
        line = line.strip()
        if line == '':
            continue
        parts = line.split('=')
        if len(parts) != 2:
            raise SyntaxError("failed to parse line {} '{}'".format(line_num, line))
        key = parts[0].strip()
        value = parts[1].strip()
        values[key] = value

    keys = []
    if kind == 'wrap-git':
        keys = ['directory', 'url', 'revision']
    else:
        keys = ['directory', 'source_url', 'source_filename', 'source_hash']
    for key in keys:
        if not key in values:
            raise SyntaxError("missing expected field in wrap file '{}'".format(key))
        setattr(wrap, key, values[key])
    if kind == 'wrap-git':
        if '/' in wrap.revision:
            raise SyntaxError("invalid revision '{}'".format(wrap.revision))
    return wrap


def extract_value_from_wrap(wrap_path, key_name):
    f = open(wrap_path, 'r')
    for line in f.readlines():
        parts = line.split('=')
        if len(parts) != 2:
            continue
        key = parts[0].strip()
        value = parts[1].strip()
        if key == key_name:
            return value
    return None
