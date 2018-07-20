#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import datetime
import subprocess

did = os.path.expanduser('~/did.txt')

def current_date():
    t = datetime.date.today()
    today = '%s %s %s %s' %(t.strftime("%A") + ',', t.day, t.strftime("%B"), t.year)
    return today

def touch():
    did_here = subprocess.call(['test', '-e', did])
    if did_here is 1:
        subprocess.call(['touch', did])

def append_date():
    date_appended = subprocess.call(['grep', '-q', current_date(), did])
    if date_appended is 1:
        with open(did, 'a') as file:
            if os.stat(did).st_size == 0:
                file.write(current_date())
            else:
                file.write('\n' + current_date())

def get_line_count():
    return sum(1 for line in open(did))

def main():
    touch()
    append_date()
    subprocess.call(['nano', '+' + str(get_line_count() + 1), did])

if __name__ == '__main__':
    main()