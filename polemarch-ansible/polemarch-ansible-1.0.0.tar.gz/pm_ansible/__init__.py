'''
Wrapper for Ansible cli.

Usage:
*  `pm-execute [ansible command name] [args]` - calls any ansible cli tool.
*  `pm-cli-reference [ansible command name,...] [--exclude key]` -
    output cli keys for command. Default - all. Exclude keys by names (support many).
'''

__version__ = '1.0.0'
