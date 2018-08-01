#!/usr/bin/env python3

from distutils.core import setup

MAJOR_VERSION='0'
MINOR_VERSION='0'
PATCH_VERSION='1'

VERSION = "{}.{}.{}".format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)

packages = ['sneks']
package_dir = {p: 'src/' + p for p in packages}

def main():
    setup(
        name = 'sneks',
        packages = packages,
        package_dir = package_dir,
        version = VERSION,
        description = 'Basic python utilities.',
        author = 'Steve Norum',
        author_email = 'sn@drunkenrobotlabs.org',
        url = 'https://github.com/stevenorum/sneks',
        download_url = 'https://github.com/stevenorum/sneks/archive/{}.tar.gz'.format(VERSION),
        keywords = ['python'],
        classifiers = [],
    )

if __name__ == "__main__":
    main()
