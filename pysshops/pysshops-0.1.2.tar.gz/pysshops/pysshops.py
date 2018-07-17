#! /usr/bin/env python

import logging
from paramiko import SSHClient, WarningPolicy
from socket import error, herror, gaierror, timeout


logger = logging.getLogger('pysshops')


class SshOps:
    hostname = ""
    username = ""
    ssh = None

    def __init__(self, hostname, username):
        """ init a hostname and username for ssh connection """
        self.hostname = hostname
        self.username = username

    def __enter__(self):
        """ get a ssh connection to hostname """
        logger.info('opening ssh connection to %s' % self.hostname)
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(WarningPolicy())
        try:
            ssh.connect(self.hostname, username=self.username)
        except (error, herror, gaierror, timeout) as neterr:
            msg = 'network problem: %s' % (neterr)
            logger.error(msg)
            raise SshNetworkException(msg)
        self.ssh = ssh
        return self

    def __check_exit(self, exitcode, stdout, stderr, block=True):
        """ check the exit code and if not 0 log stderror and exit
        (if blocking command) """
        if exitcode == 0:
            return
        else:
            msg = 'ssh command failed with exit code %s: %s' \
                   % (str(exitcode), stderr)
            logger.error(msg)
            if block:
                raise SshCommandBlockingException(msg)

    def remote_command(self, command, block=True):
        """ execute a remote command by the ssh connection """
        logger.debug(command)
        stdin, stdout, stderr = self.ssh.exec_command(command)
        stdout_str = ' ,'.join(stdout.readlines())
        stderr_str = ' ,'.join(stderr.readlines())
        logger.debug('stdout: ' + stdout_str)
        logger.debug('stderr: ' + stderr_str)
        return self.__check_exit(stdout.channel.recv_exit_status(),
                                 stdout_str,
                                 stderr_str,
                                 block)

    def __exit__(self, exc_type, exc_value, traceback):
        """ close the ssh connection at the end """
        self.ssh.close()


class SftpOps:
    hostname = ''
    username = ''
    ssh = None
    sftp = None

    def __init__(self, hostname, username):
        """ init a hostname and username for sftp connection """
        self.hostname = hostname
        self.username = username

    def __enter__(self):
        """ get a sftp connection to hostname """
        logger.info('opening sftp connection to %s' % self.hostname)
        ssh = SSHClient()
        sftp = None
        ssh.set_missing_host_key_policy(WarningPolicy())
        try:
            ssh.connect(self.hostname, username=self.username)
            sftp = ssh.open_sftp()
        except (error, herror, gaierror, timeout) as neterr:
            msg = 'network problem: %s' % (neterr)
            logger.error(msg)
            raise SftpNetworkException(msg)
        self.ssh = ssh
        self.sftp = sftp
        return self

    def deploy(self, src, dst, block=False):
        """ deploy a local file to remote host """
        try:
            self.sftp.put(src, dst)
        except Exception as ex:
            msg = 'SFTP deploy exception: %s' % (ex)
            logger.error(msg)
            if block:
                raise SftpCommandException(msg)

    def chmod(self, dst, block=False):
        """ chmod of a remote file """
        try:
            self.sftp.chmod(dst)
        except Exception as ex:
            msg = 'SFTP chmod exception: %s' % (ex)
            logger.error(msg)
            if block:
                raise SftpCommandException(msg)

    def __exit__(self, exc_type, exc_value, traceback):
        """ close the sftp connection at the end """
        self.sftp.close()
        self.ssh.close()


class SshNetworkException(Exception):
    pass


class SshCommandBlockingException(Exception):
    pass


class SftpNetworkException(Exception):
    pass


class SftpCommandException(Exception):
    pass
