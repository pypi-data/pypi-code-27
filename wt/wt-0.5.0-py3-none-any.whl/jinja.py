# -*- coding: utf-8 -*-

import os

import jinja2
import markdown


class Registry(object):

    def __init__(self):
        self._functions = []

    def add(self, fn):
        self._functions.append(fn)
        return fn

    def __iter__(self):
        for fn in self._functions:
            yield fn


filters = Registry()
functions = Registry()


def get_env(workdir, **config):
    loader = jinja2.ChoiceLoader([
        jinja2.FileSystemLoader(
            os.path.join(workdir, 'templates')),
        jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates'))
    ])
    md_exts = config.pop('markdown_extensions', [])
    env = jinja2.Environment(loader=loader, **config)
    env.add_extension('jinja2.ext.autoescape')

    try:
        import jinja_helpers  # noqa
    except ImportError:
        pass

    for fn in filters:
        if not hasattr(fn, 'filter_name') and not hasattr(fn, '__name__'):
            raise ValueError(
                'Registered jinja filter must be a function '
                'or must have "filter_name" attribute')
        env.filters[getattr(fn, 'filter_name',
                            getattr(fn, '__name__', 'fltr'))] = fn

    for fn in functions:
        if not hasattr(fn, 'function_name') and not hasattr(fn, '__name__'):
            raise ValueError(
                'Registered jinja function must be a real function '
                'or must have "function_name" attribute')
        env.globals[getattr(fn, 'function_name',
                            getattr(fn, '__name__', 'func'))] = fn

    if 'markdown' not in env.filters:

        def md(text):
            return markdown.markdown(text,
                                     extensions=md_exts,
                                     output_format='html5')

        env.filters['markdown'] = md
    return env
