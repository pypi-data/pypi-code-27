import boto3
import click
import configparser
import os

class Challenge(object):

    title = 'fake'
    description = 'fake'
    track_name = ''
    track_id = ''

    def __init__(self, track_id, track_name):
        self.track_name = track_name
        self.track_id = track_id

    def help(self):
        self.instructions()

    def start(self):
        self.instructions()
    
    def instructions(self):
        """ Prints the instructions of a challenge """
        click.echo(click.style("\n> Challenge: {}\n".format(self.title), fg='blue', bold=True))
        click.echo(click.style(self.description, fg='black'))
        command = click.style("awslabs {}".format(self.track_id), bold=True)
        click.echo("When finished type: {} to validate your progress.\n\n".format(command))

    def fail(self, description):
        """ Prints the FAILED message and returns False """
        click.echo(click.style("\n{}\n".format("CHALLENGE FAILED"), fg='red'))
        click.echo(click.style("  {}\n".format(description), fg='black'))
        click.echo(click.style("{}\n".format("Try again!"), fg='black'))
        return False
    
    def success(self, description):
        """ Prints the SUCCESS message and returns True """
        click.echo(click.style("\n{}\n".format("CHALLENGE SUCCESS"), fg='green'))
        click.echo(click.style(description, fg='black'))
        return True

    def save(self, key, value):
        """ Save a value to the config file of this Track """
        file = '~/.awslabs/config'
        filename = os.path.expanduser(file)
        config = configparser.ConfigParser()
        config.read(filename)
        config.set(self.track_id, key, value)
        with open(filename, 'w') as fp:
            config.write(fp)
    
    def get(self, key):
        """ Get a value from the config file of this Track """
        file = '~/.awslabs/config'
        filename = os.path.expanduser(file)
        config = configparser.ConfigParser()
        config.read(filename)
        return config[self.track_id][key]
    
    def debug(self, text):
        if os.environ["AWSLABS_VERBOSE"] == "1":
            click.echo("INFO: {}".format(text))