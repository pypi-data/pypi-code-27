#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

from .ssh import SshHost, SshClient


def __execute(interactive, cmd):
    if interactive is None:
        res = subprocess.run(cmd.split(" "), stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
        if res.returncode != 0:
            raise RuntimeError("command return code is not zero.")
        return res.stdout.decode(encoding="utf-8")
    _, stdout, stderr = interactive.exec_command(cmd)
    if stdout.channel.recv_exit_status() != 0:
        raise RuntimeError("command return code is not zero.")
    return stdout


def execute(host: SshHost, *cmdline, display=False):
    result = []

    def exec_impl(sct):
        for cmd in cmdline:
            print("$ {}".format(cmd))
            stdout = __execute(sct.ssh if sct is not None else None, cmd)
            if display:
                print(stdout)
            result.append(stdout)

    if host.is_localhost:
        sc = None
        exec_impl(sc)
    else:
        sc = SshClient(host)
        with sc:
            exec_impl(sc)
    return result
