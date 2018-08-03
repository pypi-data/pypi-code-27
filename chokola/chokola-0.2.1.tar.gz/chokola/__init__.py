import yaml, re, textwrap
import yamlordereddictloader

from .renderer import Renderer
from .formatter import Formatter
from .table import Table


def call(source):
    with open(source, 'r') as stream:
        data = yaml.load(stream.read(), Loader=yamlordereddictloader.Loader)
        table = call_data(data)
        print(table)


def call_data(data, formatter=Formatter()):
    renderer = Renderer(formatter)
    table = Table(renderer=renderer)
    return table(data)