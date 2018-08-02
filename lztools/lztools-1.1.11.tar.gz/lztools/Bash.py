import os
from pathlib import Path
from subprocess import run

from lztools import text

def command_result(name, *args):
    try:
        result = run([name, *args], capture_output=True, universal_newlines=True, check=True)
        # x = check_output([name, *args], universal_newlines=True)
        #
        # Popen()
        return result.stdout
    except:
        raise

# def command(command):
#     os.system(command)

def command(command, *args):
    fargs = " ".join(args)
    os.system(f"{command} {fargs}")

def apt_install(package):
    command(f"sudo apt install -y {package}")


def get_history():
    return command_result("cat", "{}/.bash_history".format(str(Path.home())))

def search_history(term, regex=False):
    if not regex:
        for line in get_history().splitlines():
            if term in line:
                yield line
    else:
        return text.regex(term, get_history())
