"""
Leonard always DRIVES Sheldon (this module is the __main__ driver for Sheldon)
"""
import argparse
import sys
import os

try:
    from cooper import Sheldon
except:
    from .cooper import Sheldon

# Extensions for python source files
EXTENSIONS = [".py", ".mpy"]

def parseargs():
    """parse the command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-hr", "--human_readable",
                        help="set for friendlier output",
                        action="store_true")
    parser.add_argument("-r", "--recursive",
                        help="recursively check python files in path",
                        action="store_true")
    parser.add_argument("path",
                        type=str,
                        help="path to python source file(s)")
    return parser.parse_args()

def procfiles(files, divs_found, readable, path=""):
    """function to process the python source files"""
    if files:
        for filename in files:
            fname = os.path.join(path, filename)
            with open(fname) as f:
                pysource = f.read()
                s = Sheldon(pysource)
                try:
                    s.analyze()
                except SyntaxError:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    print(f"{fname} {exc_tb.tb_lineno} SyntaxError")
                    continue
                divs_found += len(s.divisions)
                s.printdivs(fname, s.divisions, readable)
    return divs_found

def main():
    ARGS = parseargs()

    if ARGS.human_readable:
        def readableprint(*args, **kwargs):
            print(*args, **kwargs)
    else:
        readableprint = lambda *a, **k: None # do - nothing function

    files_checked = 0
    divs_found = 0

    # Directory path
    if os.path.isdir(ARGS.path):
        for path, dirs, files in os.walk(ARGS.path):
            files = [f for f in os.listdir(path) if f.endswith(tuple(EXTENSIONS))]
            files_checked += len(files)

            divs_found = procfiles(files, divs_found, ARGS.human_readable, path=path)

            if not ARGS.recursive:
                exit(0)

        readableprint(f"{files_checked} files checked")
        readableprint(f"{divs_found} divisions found")

    # File path
    elif os.path.isfile(ARGS.path):
        files =[f for f in [ARGS.path] if ARGS.path.endswith(tuple(EXTENSIONS))]

        divs_found = procfiles(files, divs_found, ARGS.human_readable)

        readableprint(f"{divs_found} divisions found")

    # Error
    else:
        sys.exit(f"{ARGS.path} doesn't exist!")

if __name__ == "__main__":
    main()
