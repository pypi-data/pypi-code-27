# -*- coding: utf-8 -*-
from pyramid.config import Configurator


def app(global_config, **settings):
    """Return the Pyramid WSGI application."""
    config = Configurator(settings=settings)
    config.include("pyramid_jinja2")
    config.add_static_view("static", "static", cache_max_age=3600)
    config.include("potemkin.routes")
    config.scan()
    return config.make_wsgi_app()
