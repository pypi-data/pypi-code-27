# pylistmanager
# Copyright (C) 2018  Sotiris Papatheodorou
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-


def input_int(prompt='', min_value=0, max_value=1):
    while True:
        try:
            i = int(input(prompt))
            if i < min_value or i > max_value:
                raise ValueError
            break
        except ValueError:
            print('Enter an integer between ' + str(min_value)
                  + ' and ' + str(max_value))
    return i

def input_yn(prompt=''):
    valid_answers = ['y', 'Y', 'yes', 'Yes', 'YES', 'n', 'N', 'no', 'No', 'NO']
    while True:
        try:
            s = input(prompt)
            if s not in valid_answers:
                raise ValueError
            break
        except ValueError:
                print('Enter y or n')
    if s in valid_answers[0:4]:
        return True
    else:
        return False

