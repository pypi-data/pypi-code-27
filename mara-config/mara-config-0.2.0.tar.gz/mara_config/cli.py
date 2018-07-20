import click
import sys

@click.group(invoke_without_command=False, name='config')
def mara_config():
    """mara_config related commands"""
    pass

@mara_config.command()
def print():
    """Prints the current config"""
    from mara_config.config_system.config_display import print_config
    print_config()


@mara_config.command()
def generate_local_setup():
    """Generates a basic setup_local.py which can be adjusted.

    Use like `mara config generate_local_setup >> app/local_setup.py`
    """
    from mara_config.config_system.config_display import generate_local_setup
    lines = generate_local_setup()
    click.echo('\n'.join(lines))

@mara_config.command()
def validate():
    """Validates the current config

    If a validation errors exists, prints them to stderr and exits 1
    """
    from mara_config.config_system.config_display import validate_config
    validation_errors = validate_config()
    if validation_errors:
        click.echo('\n'.join(validation_errors), err=True)
        sys.exit(1)
