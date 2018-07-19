#!/usr/bin/python3

# import subprocess
import os
import gnupg


class Fields(dict):
    def __init__(self, string: str):
        lines = string.splitlines()
        self.pwd = lines.pop(0)

        for line in lines:
            key, _, value = line.partition(':')
            self[key] = value.lstrip()


PASS_PATH = os.path.expanduser('~/.password-store/')
_gpg = gnupg.GPG()


def get(passname):
    with open(PASS_PATH + passname + '.gpg', 'rb') as f:
        crypt = _gpg.decrypt_file(f)
    info = str(crypt)

    return Fields(info)


if __name__ == '__main__':
    print(get('work/mikro.mikroelektronika.cz'))
