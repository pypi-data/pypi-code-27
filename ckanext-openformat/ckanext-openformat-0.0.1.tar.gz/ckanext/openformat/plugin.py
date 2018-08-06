# encode utf-8

import ckan.plugins as plugins
from ckan.controllers.package import PackageController
from ckan.config.routing import SubMapper
from ckanext.openformat.plugin import *

import requests
from flask import request
import mimetypes
from urlparse import urlparse
from os.path import splitext

class OpenformatPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IConfigurer)

    def update_config(self, config):
	pass

    def before_map(self, map):
        map.connect('/dataset/new_resource/{id}', controller='ckanext.openformat.controllers:NewController', action='new_resource')
        return map

    def after_map(self, map):
        return map
