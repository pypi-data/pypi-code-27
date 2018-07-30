#!/usr/bin/env python3
import click
from .rdt import rdt

class rdt_cli:
    @click.group()
    def begin():
        '''
        A little tool that lets you browse Reddit via Command Line
        '''

    @begin.command()
    @click.option('--move', type = click.Choice(['next', 'previous']), help = 'Move to the next or previous set of outputs')
    @click.option('--subreddits', is_flag = True, help = 'List all public subreddits available on reddit')
    @click.option('--sort', type = click.Choice(['hot', 'new', 'controversial', 'top', 'rising']), help = 'Sorts the list by hot/new/controversial/top/rising')
    def ls(move, subreddits, sort):
        '''
        List posts from the the specified subreddit or the front page if no subreddit specified and sorts by optional hot(default), new, rising, top, controversial.
        '''
        rdt.ls(move, subreddits, sort)

    @begin.command()
    @click.option('--index',default = '', help = 'Provide a specific index to view')
    @click.option('--comments', is_flag = True, help = 'View the comments of a specified post index')
    @click.option('--more-comments', is_flag = True, help = 'Load more comments from the post scope if there are posts to load')
    def view(index, comments, more_comments):
        '''
        Opens the link of the specified post index in a browser window or Loads the comments of the specified post index.
        '''
        rdt.view(index, comments, more_comments)

    @begin.command()
    @click.argument('input')
    def search(input):
        '''
        Searches reddit for the specified search term.
        '''
        rdt.search(input)

    @begin.command()
    def clear():
        '''
        Clears the entire screen.
        '''
        click.clear()
