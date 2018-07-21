from mara_cli.cli import cli, setup_commandline_commands
import re
import os

import mara_config

# needed workaorund because mara expects a MARA_APP be importable
os.environ['MARA_APP'] = 'mara_cli'


def test_print_config(cli_runner):
    # needed to get the debug into the config ouput
    mara_config.register_functionality(mara_config)
    # Needed to get the click commands registered
    setup_commandline_commands()
    result = cli_runner.invoke(cli , ['config', 'print'])
    assert result.exit_code == 0
    assert 'Config:' in result.output
    assert re.search(r'debug.+-D--.+->.+False',result.output) is not None

def test_print_config_debug(cli_runner):
    mara_config.register_functionality(mara_config)
    # Needed to get the click commands registered
    setup_commandline_commands()
    # unfortunately, you cannot simply specify ['--debug', 'config', 'print']
    # because '--debug is handled outside of click
    mara_config.set_config('debug', function=lambda: True)
    result = cli_runner.invoke(cli , ['config', 'print'])
    #assert result.exit_code == 0
    assert 'Config:' in result.output
    print(result.output)
    assert re.search(r'debug.+SD--.+->.+True',result.output) is not None
