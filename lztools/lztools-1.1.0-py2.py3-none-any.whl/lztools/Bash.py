from subprocess import check_output

import os

def command_result(name, *args):
    x = check_output([name, *args], universal_newlines=True)
    return x.strip()

# def command(command):
#     os.system(command)

def command(command, *args):
    fargs = " ".join(args)
    os.system(f"{command} {fargs}")

def apt_install(package):
    command(f"sudo apt install -y {package}")


def load_words():
    res = command_result("cat", "/usr/share/dict/words")
    return res
