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
        click.echo(click.style("Challenge: " + self.title, fg='blue'))
        click.echo(click.style(self.description, fg='black'))
        command = click.style("awslabs {}".format(self.track_id), bold=True)
        click.echo("When finished type: " + command)

    def fail(self, description):
        """ Prints the FAILED message and returns False """
        click.echo(click.style("FAILED", fg='red'))
        click.echo(click.style(description, fg='black'))
        return False
    
    def success(self, description):
        """ Prints the SUCCESS message and returns True """
        click.echo(click.style("SUCCESS", fg='green'))
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