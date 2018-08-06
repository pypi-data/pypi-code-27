"""Comment 1"""
import sys

def print_lol(the_list, indent=False, level=0, fh=sys.stdout):
    """Comment 2"""
    for item in the_list:
        if isinstance(item, list):
            print_lol(item, indent, level + 1, fh)
        else:
            if indent:
                for t in range(level):
                    print("\t", end=' ', file=fh)
            print(item, file=fh)
