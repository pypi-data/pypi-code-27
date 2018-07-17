from loggui import GUILoggerHandler
import logging
import importlib
import sys

def load(path):
    spec = importlib.util.spec_from_file_location("__main__", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

def main():
    print("LogGui run")
    path = " ".join(sys.argv[1:])
    rl = logging.getLogger()
    rl.setLevel(1)
    rl.addHandler(GUILoggerHandler(path))
    print("Executing module")
    load(path)


if __name__ == '__main__':
    main()