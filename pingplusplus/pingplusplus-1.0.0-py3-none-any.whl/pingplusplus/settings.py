import os
from configparser import ConfigParser
from threading import Event
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, SUPPRESS


def get_argument_parser():
    parser = ArgumentParser(
        description='Ping++',
        formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--interval', type=int, help='ping interval [seconds]', default=SUPPRESS)
    parser.add_argument('-t', '--timeout', type=int, help='ping timeout [seconds]', default=SUPPRESS)
    parser.add_argument('-c', '--config', type=str, default='config.ini', help='configfile')
    #parser.add_argument('-r', '--report', type=str, default='report.html', help='reportfile')
    parser.add_argument('--hosts', action='store_true', help='Parse hosts file')
    args = parser.parse_args()
    return args


def get_settings(args):

    # default values:
    settings = Settings(
        args.config,
        "", # args.report,
        interval=5,
        timeout=2
    )
    
    # override with values from arguments
    if 'interval' in args:
        settings.setstr('general', 'interval', str(args.interval))

    if 'timeout' in args:
        settings.setstr('general', 'timeout', str(args.timeout))
    
    if args.hosts:
        for host in parse_hosts_file():
            if host:
                settings.setstr('hosts', host, "")

    return settings


class Settings():

    def __init__(self, configfile, reportfile, interval, timeout):

        self.root_dir = os.path.dirname(__file__)

        settings = ConfigParser(allow_no_value=True, delimiters="=")
        settings.add_section("general")
        settings.add_section("hosts")
        settings["general"]["timeout"] = str(timeout)
        settings["general"]["interval"] = str(interval)
        settings["general"]["warning_limit"] = "100"
        settings["general"]["logfile"] = "ping_log.csv"
        settings["general"]["csvfilepath"] = "."
        #settings["general"]["reportfile"] = reportfile

        settings.read(os.path.join(self.root_dir, 'default.ini'))
        # settings.read(os.path.join(self.root_dir, 'config.ini'))
        settings.read(configfile)

        self._configfile = configfile
        self._settings = settings

        self.hasChanged = Event()
        self.hasChanged.set()

    def getlist(self, section):
        return self._settings[section]

    def getfloat(self, section, key):
        return self._settings.getfloat(section, key)

    def getstr(self, section, key):
        return self._settings[section][key]

    def setstr(self, section, key, val):
        self._settings.set(section, key, val)
        self.hasChanged.set()

    def save(self):
        with open(self._configfile, "w") as f:
            self._settings.write(f, space_around_delimiters=False)


def parse_hosts_file():
    if os.name == 'posix':
        hostsfile = '/etc/hosts'
    elif os.name == 'nt':
        hostsfile = 'C:/windows/system32/drivers/etc/hosts'
    else:
        hostsfile = ''
    if hostsfile and os.path.isfile(hostsfile):
        with open(hostsfile, 'r') as f:
            for line in f.readlines():
                comment = line.find("#")
                if comment == -1:
                    yield line.replace("\t", " ").strip()
                else:
                    yield line[:comment].replace("\t", " ").strip()
    return ''
