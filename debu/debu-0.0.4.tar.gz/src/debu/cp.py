#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
import tempfile
import random
import pathlib

from .ssh import SshHost, SshClient


def __normalization(path: str, cwd: str):
    cwd = pathlib.Path(cwd)
    path = pathlib.Path(path)
    if path.is_absolute():
        return str(cwd / path)
    return str(path)


def copy(dst_host: SshHost, dst_path: str, src_host: SshHost, src_path: str, working_directory=str(pathlib.Path.cwd())):
    if dst_host.is_localhost and src_host.is_localhost:
        shutil.copy(__normalization(src_path, working_directory), __normalization(dst_path, working_directory))
        return

    if dst_host.is_localhost and not src_host.is_localhost:
        sc = SshClient(src_host)
        with sc:
            sftp = None
            try:
                sftp = sc.ssh.open_sftp()
                dst_path = __normalization(dst_path, working_directory)
                sftp.get(src_path, dst_path)
            finally:
                if sftp is not None:
                    sftp.close()
        return

    if not dst_host.is_localhost and src_host.is_localhost:
        sc = SshClient(dst_host)
        with sc:
            sftp = None
            try:
                src_path = __normalization(src_path, working_directory)
                sftp = sc.ssh.open_sftp()
                sftp.put(src_path, dst_path)
            finally:
                if sftp is not None:
                    sftp.close()
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = temp_dir + "/" + str(random.random())
        copy(SshHost.localhost(), temp_file, src_host, src_path)
        copy(dst_host, dst_path, SshHost.localhost(), temp_file)
