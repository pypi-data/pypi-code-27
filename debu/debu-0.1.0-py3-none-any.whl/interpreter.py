#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import typing
import re
import sys
import pathlib
import argparse

from .ssh import SshHost
from .cp import copy
from .execute import execute


class ExecuteInfo:
    def __init__(self, show_variables=False):
        self.__variable = {}
        self.__show_variables = show_variables

    def __getitem__(self, key: str):
        return self.__variable[key]

    def __setitem__(self, key, value):
        if self.__show_variables:
            print("    {} = {}".format(key, value))
        self.__variable[key] = value

    def has(self, key):
        return key in self.__variable


def __decode_rvalue(info: ExecuteInfo, rvalue: str):
    if "@" in rvalue:
        rr = [r.strip() for r in rvalue.split("@")]
        user = rr[0]
        host = rr[1]
        port = 22
        if info.has(rr[0]):
            user = info[rr[0]]

        match = re.match("(\[(.+)\]|[0-9A-Za-z.]+):(\d+)$", host)
        if match is not None:
            host = match.group(1)
            port = match.group(2)
        return SshHost(host, user, port)
    if info.has(rvalue):
        rvalue = info[rvalue]

    elif rvalue[0] == rvalue[-1] == '"':
        rvalue = rvalue[1:-1]
    elif rvalue.startswith("0x"):
        rvalue = int(rvalue[2:], 16)
    elif rvalue.startswith("0o"):
        rvalue = int(rvalue[2:], 8)
    elif rvalue.startswith("0b"):
        rvalue = int(rvalue[2:], 2)
    else:
        rvalue = int(rvalue)
    return rvalue


def __exec(info: ExecuteInfo, src: str):
    if "=" in src:
        ss = [s.strip() for s in src.split("=")]
        info[ss[0]] = __decode_rvalue(info, ss[1])
        return None

    if ":" in src:
        src = [s.strip() for s in src.split(":")]
        target = src[0]
        command = [s.strip() for s in src[1].split(" ")]

        if ">>" in target and command[0] in ["cp", "copy", "scp"]:
            if len(command) > 3:
                raise RuntimeError("too few arguments.\ncopy command must have source path and destination path")

            target = [s.strip() for s in target.split(">>")]
            src = __decode_rvalue(info, target[0])
            dst = __decode_rvalue(info, target[1])
            if not isinstance(src, SshHost) or not isinstance(dst, SshHost):
                raise TypeError("target must be ssh host")

            return lambda: copy(dst, command[2], src, command[1])

        target = __decode_rvalue(info, target)
        if not isinstance(target, SshHost):
            raise TypeError("target format is 'target' or 'destination << source'")

        return lambda: execute(target, *command, display=True)

    command = [s.strip() for s in src.split(" ")]
    if command[0] in ["print", "echo"]:
        content = ""
        if len(command) > 1:
            content = __decode_rvalue(info, command[1])
        return lambda: print(content)

    raise RuntimeError("unknown command. {}".format(src))


def interpret(src: typing.List[str], check_only=False, show_variables=False):
    info = ExecuteInfo(show_variables)
    recipe = []

    print(">> Checking source...")
    info["localhost"] = SshHost.localhost()
    info["working_directory"] = str(pathlib.Path.cwd())
    for i, s in enumerate(src, 1):
        if "#" in s:
            s = s[:s.find("#")]
        if len(s.strip()) == 0:
            continue

        try:
            recipe.append(__exec(info, s))
        except Exception as e:
            print("Raised in line {}".format(i), file=sys.stderr)
            print("Execute abort", file=sys.stderr)
            print("Message:", e, file=sys.stderr)
            exit(1)

    print("<< Check passed ({} commands)".format(len(recipe)))

    if not check_only:
        print(">> Executing...")
        [f() for f in recipe if f is not None]


def main():
    parser = argparse.ArgumentParser(
        prog="debu",
        usage="PROGRAM SOURCE_FILE",
        description="Interpreter for Automatic Deploy and Build system",
        epilog="Apache License 2.0"
    )
    parser.add_argument("source", action="store", type=str, help="debu script file")
    parser.add_argument("--check", "-t", "-c", action="store_true", help="Syntax check mode (do not execute)")
    parser.add_argument("--variables", "--trace-variables", "-v", action="store_true", help="Display all variables")

    args = parser.parse_args()

    with open(args.source) as fp:
        interpret(fp.readlines(), check_only=args.check, show_variables=args.variables)


if __name__ == '__main__':
    main()
