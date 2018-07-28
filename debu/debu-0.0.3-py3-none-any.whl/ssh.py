#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass

from paramiko import SSHClient, AutoAddPolicy


class SshHost:
    def __init__(self, host, user, password=None, key=None, port=22, passphrase=None):
        self.__host = host
        self.__user = user
        self.__port = port
        if password is None and key is None:
            password = getpass.getpass("Password ({}@{}): ".format(self.__user, self.__host))
        self.__password = password
        self.__key = key
        self.__passphrase = passphrase

    @staticmethod
    def localhost():
        return SshHost("localhost", getpass.getuser(), "", None)

    @property
    def host(self):
        return self.__host

    @property
    def user(self):
        return self.__user

    @property
    def password(self):
        return self.__password

    @property
    def port(self):
        return self.__port

    @property
    def key(self):
        return self.__key

    @property
    def is_localhost(self) -> bool:
        return self.__host in ["localhost", "127.0.0.1"]

    @property
    def passphrase(self):
        return self.__passphrase

    def __str__(self):
        return "{}@{}:{}".format(self.user, self.host, self.port)


class SshClient:
    def __init__(self, host: SshHost):
        self.__host = host

    def __enter__(self):
        self.__ssh = get_ssh_client(self.__host)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__ssh.close()

    @property
    def ssh(self):
        return self.__ssh


def get_ssh_client(host: SshHost):
    ssh = SSHClient()

    ssh.set_missing_host_key_policy(AutoAddPolicy())

    ssh.connect(host.host, host.port,
                host.user, password=host.password, key_filename=host.key, passphrase=host.passphrase)

    return ssh
