import click
import importlib
import os
from awslabs.tracks.s3.mytrack import MyTrack

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

def load_class(full_class_string):
    """
    dynamically load a class from a string
    """

    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('track')
@click.argument('action', default='validate', type=click.Choice(['start', 'validate', 'help', 'stop', 'restart']))
def main(track = '', action = ''):

    try:
        trackClass = load_class('awslabs.tracks.{}.mytrack.MyTrack'.format(track))(track)
    except:
        print('Track {} not found'.format(track))
        exit()
    
    getattr(trackClass, action)()


if __name__ == '__main__':
    main()