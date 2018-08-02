import os
from IPython.display import display, Markdown


class Info:
    def __init__(self,name):
        self.name=name+'.md'

    def info(self):
        _dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(_dir, 'markdown', self.name)
        with open(path, 'r') as f:
            md = f.read()
            display(Markdown(md))
