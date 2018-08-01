import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """lztools for git"""

@main.command(context_settings=CONTEXT_SETTINGS)
def branch():
    """Branch operations"""