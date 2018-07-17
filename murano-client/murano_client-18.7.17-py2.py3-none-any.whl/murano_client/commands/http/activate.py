# pylint: disable=C0325,C0103
from murano_client.commands.http import Command as ExositeConnection
from murano_client.commands import build_api_opts_from_docopt_args

class ExoCommand(ExositeConnection):
    """Use the HTTP Device API to activate client described by Product
and Device IDs. Prints the CIK to STDOUT if successful. If -f option is
used, the Device config file is used.

  usage:
    activate [options]

  options:
    -h --help                   Show this screen.

    """
    Name = 'activate'
    def execute(self):
        from murano_client.http import MuranoHTTP
        from murano_client.ini import Device

        if self.global_args.get('--file'):
            d = Device(self.global_args.get('--file'))
            d.activate_device()
            if d.is_activated():
                pass
            else:
                print("Activation attempt not successful.")
            with open(self.global_args.get('--file'), 'r') as f:
                print(f.read())
        else:
            api = MuranoHTTP(**build_api_opts_from_docopt_args(self.global_args))
            api.http_activate()
            print(api.murano_token())
            if not api.is_activated():
                print("activation not successful")
