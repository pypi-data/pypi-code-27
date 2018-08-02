import click
from lztools.text import regex

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("expr")
@click.argument("text", default=click.get_text_stream('stdin'))
@click.option("-s", "--single-result", is_flag=True, default=False)
def main(expr, text, single_result):
    """Regex using python"""
    for res in regex(expr, text):
        print(res)
        if single_result:
            break