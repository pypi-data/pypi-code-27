# -*- coding: utf-8 -*-


def includeme(config):
    config.add_route("ltilaunch_iframe", "/")
    config.add_route("ltilaunch_form", "/form")
    config.add_route("ltilaunch_sign", "/sign")
