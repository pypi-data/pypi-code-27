#!/opt/util/oitnb/bin/python

"""

assumes that it starts in a temporary directory with two directories that can be converted

add to your .hgrc:

[extensions]
hgext.extdiff =

[extdiff]
cmd.omeld =


"""

import sys
import os


def main():
    assert len(sys.argv) == 3, 'omeld: expecting two arguments'
    for idx, arg in enumerate(sys.argv[1:]):
        assert os.path.exists(
            sys.argv[1]
        ), f'omeld: expecting a directory as parameter {idx}, cannot find "{arg}"'
        assert os.path.isdir(
            sys.argv[1]
        ), f'omeld: expecting a directory as parameter {idx}, got "{arg}"'
    # check if you are on a temporary directory, so there is less chance to screw up
    assert '/tmp/' in os.getcwd(), 'omeld: for safety only runs when PWD includes "/tmp/"'
    os.system('oitnb -q .')
    os.system('meld ' + ' '.join(sys.argv[1:]))


if __name__ == '__main__':
    main()
