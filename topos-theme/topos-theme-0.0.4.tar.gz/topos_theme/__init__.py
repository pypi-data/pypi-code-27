from os import path


__version__ = "0.0.4"


def setup(app):
    app.add_html_theme('topos-theme', path.abspath(path.dirname(__file__)))
