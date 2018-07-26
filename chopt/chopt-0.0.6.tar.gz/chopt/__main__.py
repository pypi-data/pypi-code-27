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
    if chosen:
        print("\nChosen items: " + ", ".join(chosen) + "\n")
    else:
        print("\nNothing to see here.\n")


if __name__ == '__main__':
    main()
