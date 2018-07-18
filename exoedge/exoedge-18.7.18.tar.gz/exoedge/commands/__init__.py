# pylint: disable=W1202
"""
Namespace for ExoEdge commands.

TODO: Clear this out
"""

import sys
# import six
import docopt
import logging

LOG = logging.getLogger(name='GDC.HTTP')


class Command(object):  # ExositeConnection
    """Use methods of the HTTP(S) Device API.

  usage:
    http <command> [<args>...]

  commands:
    timestamp         Get the Murano timestamp.
    activate          Get a CIK/Token from a Murano Product for an id.
    read              Read resource described by <alias>.
    poll              Long poll <alias> for <request-timeout> since <if-modified-since>.
    write             Write <value> to <alias> resource.
    record            Record <value> to <alias> at time <timestamp>.
    content           Download content, get content info and list content.

  options:
    -N --no-ssl                 If provided, SSL/TLS will not be used in HTTP(S) comms.
    -F --no-form-encode         If provided, POST data will not be form-encoded.
    -P --no-product-domain      If provided, project domains (i.e. your project ID).
    -i --pid <id>               The Product ID.
    -t --timeout <secs>         If provided, <secs> is used as HTTP Timeout (in seconds).
                                Not implemented in Mqtt.
    -H --host <host>            If provided, <host> is used as the server hostname for
                                HTTP requests.
    -d --debug <lvl>            Turn on verbose debug output. Also logs curl commands.
    -u --uuid <uuid>            Specify the id of the connecting client (mqtt only).
    -f --file <file>            All operations will use <file> as the Device state file. This file
                                is compatible with Device class objects. Will store <cik> and
                                provision as the Murano client described in its options. This
                                option has special support for configuring the GWE config file
                                by using 'gwe' as the <file> argument.
    -C --cert <cert>            Use <cert> for Murano Provisioning of client described in
                                  the certificate subject.
    -K --pkey <pkey>            Use <pkey> in TLS communication with Murano.
    <cik>                       A CIK (Client Interface Key) or Token.
    <command>                   The HTTP(S) Device API method name.
    <args>                      Args for subcommands.

    """
    Name = 'http'
    def __init__(self, command_args, global_args):
        """
        Initialize the commands.
        :param command_args: arguments of the command
        :param global_args: arguments of the program
        """
        self.args = docopt.docopt(self.__doc__, argv=command_args, options_first=True)
        global_args.update({k:v for k, v in self.args.items() if v})
        self.global_args = global_args

        if self.global_args.get('--debug'):
            LOG.setLevel(eval('logging.'+self.global_args.get('--debug')))

    def execute(self, **exc_args):
        """Execute the commands"""
        import imp
        import os
        import pkgutil
        import murano_client.commands.http
        # Retrieve the command to execute.
        command_name = self.args.pop('<command>')
        # Retrieve the command arguments.
        command_args = self.args.pop('<args>')

        # Retrieve the module from the 'commands' package.
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'commands', Command.Name))
        try:
            http_path = murano_client.commands.http.__path__[0]
            LOG.debug('http_path: {}'.format(http_path))
            sys.path.insert(0, http_path)
            for _, module_name, _ in pkgutil.iter_modules([http_path]):
                command_path = os.path.join(http_path, command_name+'.py')
                if module_name == command_name:
                    LOG.debug('command_path: {}'.format(command_path))
                    the_module = imp.load_source(command_name, command_path)
            command_class = getattr(the_module, 'ExoCommand')

        except ImportError as exc:
            LOG.debug("{}: cannot find command {!r}: {}".format(self.Name, command_name, exc))
            raise docopt.DocoptExit()
        except AttributeError:
            LOG.debug('{}: unknown command: {}'.format(self.Name, command_name))
            raise docopt.DocoptExit()

        # Create an instance of the command and execute it
        command_class(command_args, self.global_args).execute()
