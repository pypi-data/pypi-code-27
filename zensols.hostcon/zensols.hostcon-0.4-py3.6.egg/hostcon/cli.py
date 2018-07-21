import os
from zensols.actioncli import OneConfPerActionOptionsCli
from zensols.hostcon import Connector, AppConfig

VERSION = '0.2'

class ConfAppCommandLine(OneConfPerActionOptionsCli):
    def __init__(self):
        conf_env_var='HOSTCONRC'
        if conf_env_var in os.environ:
            config_file = os.environ[conf_env_var]
        else:
            config_file = '%s/.hostconrc' % os.environ['HOME']
        host_op = ['-n', '--hostname', False,
                   {'dest': 'host_name',
                    'help': 'the host to connect to'}]
        dryrun_op = ['-d', '--dryrun', False,
                     {'dest': 'dry_run',
                      'action': 'store_true',
                      #'default': False,
                      'help': 'dry run to not actually connect, but act like it'}]
        output_file_op = ['-o', '--output', False,
                          {'dest': 'output_file',
                           'metavar': 'FILE',
                           'help': 'output file for the script actions'}]
        conf = AppConfig(config_file)
        default_action = conf.get_option('action')
        cnf = {'executors':
               [{'name': 'fixer',
                 'executor': lambda params: Connector(**params),
                 'actions':[{'name': 'info',
                             'meth': 'print_info',
                             'doc': 'print configuration info',
                             'opts': [host_op, dryrun_op]},
                             {'name': 'env',
                              'meth': 'print_environment',
                              'doc': 'print info as environment variables',
                              'opts': [host_op, dryrun_op]},
                            {'name': 'bourne',
                             'meth': 'create_bourne',
                             'doc': 'create a bourne shell script that does the same thing with the current network configuration',
                             'opts': [host_op, output_file_op]},
                            {'name': 'xterm',
                             'meth': 'exec_xterm',
                             'doc': 'start an xterm on host',
                             'opts': [host_op, dryrun_op]},
                            {'name': 'emacs',
                             'meth': 'exec_emacs',
                             'doc': 'start emacs on the host',
                             'opts': [host_op, dryrun_op]},
                            {'name': 'mount',
                             'meth': 'exec_mount',
                             'doc': 'mount directories from host locally',
                             'opts': [host_op, dryrun_op]},
                            {'name': 'umount',
                             'meth': 'exec_umount',
                             'doc': 'un-mount directories',
                             'opts': [host_op, dryrun_op]},
                            {'name': 'login',
                             'meth': 'exec_login',
                             'doc': 'slogin to host',
                             'opts': [host_op, dryrun_op]}]}],
               'config_option': {'name': 'config',
                                 'opt': ['-c', '--config', False,
                                         {'dest': 'config', 'metavar': 'FILE',
                                          'default': config_file,
                                          'help': 'configuration file'}]},
               'whine': 1}
        super(ConfAppCommandLine, self).__init__(cnf, version=VERSION, default_action=default_action)

    def _create_config(self, config_file, default_vars):
        defs = {}
        defs.update(default_vars)
        defs.update(os.environ)
        return AppConfig(config_file=config_file, default_vars=defs)

def main():
    cl = ConfAppCommandLine()
    cl.invoke()
