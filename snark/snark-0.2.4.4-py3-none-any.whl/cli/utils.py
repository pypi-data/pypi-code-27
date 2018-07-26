import snark
import pkg_resources
from outdated import check_outdated, warn_if_outdated

def get_cli_version():
    return "1.0.0" #TODO

def verify_cli_version():
    try:
        version = pkg_resources.get_distribution(snark.__name__).version
        is_outdated, latest_version = check_outdated(snark.__name__, version)
        if is_outdated:
            print('\033[93m'+"Snark is out of date. Please upgrade the package by running `pip3 install --upgrade snark`"+'\033[0m')
    except:
        pass
