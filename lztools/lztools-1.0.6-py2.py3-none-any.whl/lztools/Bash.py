from subprocess import check_output

import os

def return_command_result(name, *args):
    x = check_output([name, *args], universal_newlines=True)
    return x.strip()

def execute_command(command):
    os.system(command)

def execute_command_and_args(command, *args):
    command = "{} {}".format(command, str.join(" ", args))
    os.system(command)
