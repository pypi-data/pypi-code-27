def getargs():
    from argparse import ArgumentParser
    parser = ArgumentParser(description='Choose Options from a list.')
    parser.add_argument("options", nargs='+', help="Options for the menu.")
    return parser.parse_args()


def main():
    from .chopt import chopt
    args = getargs()
    options = args.options
    chosen = chopt(options)
    if len(chosen) > 0:
        print("Chosen items: " + ", ".join(chosen) + "\n")


if __name__ == '__main__':
    main()
