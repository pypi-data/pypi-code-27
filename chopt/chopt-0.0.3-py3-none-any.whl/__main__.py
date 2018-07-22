import argparse

from .chopt import chopt


def main():
    parser = argparse.ArgumentParser(
        description='Create a checkbox menu from a list of options.')
    parser.add_argument("options", nargs='+', help="Options for the menu.")
    args = parser.parse_args()

    options = args.options
    chosen = chopt(options)
    if len(chosen) > 0:
        print("Chosen items: " + ", ".join(chosen) + "\n")


# this means that if this script is executed, then  main() will be executed
if __name__ == '__main__':
    main()
