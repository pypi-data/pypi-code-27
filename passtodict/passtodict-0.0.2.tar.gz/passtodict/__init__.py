#!/usr/bin/python3

# import subprocess
import os
import gnupg


__all__ = ['get']


class Fields(dict):
    def __init__(self, string: str):
        lines = string.splitlines()
        self.PWD = lines.pop(0)
        self.extra = []

        for line in lines:
            key, sep, value = line.partition(':')
            if sep:
                self[key] = value.lstrip()
            else:
                self.extra.append(line)


PASS_PATH = os.path.expanduser('~/.password-store/')
gpg = gnupg.GPG()


def get(passname):
    with open(PASS_PATH + passname + '.gpg', 'rb') as f:
        crypt = gpg.decrypt_file(f)
    info = str(crypt)

    return Fields(info)


if __name__ == '__main__':
    print(get('work/mikro.mikroelektronika.cz'))
