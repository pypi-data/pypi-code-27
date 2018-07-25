import os
import pkgutil


     


class Switch(object):
    def __init__(self, app=None, blueprints_package=None):
        self._flask_app = app
        # ignore this folders to register routes
        self.ignore_list = ['core', '.vscode', 'venv', '.git', '.idea', '__pycache__']

        #: The name where blueprints are.
        self._blueprints_package = blueprints_package
        self._blueprints = []

        if app is not None:
            self.init_app(app)

    def _format_route(self, blueprint, blueprints_package=None):
        if self._blueprints_package:
            return '{0}.{1}.views'.format(blueprints_package, blueprint), blueprint
        
        return '{}.views'.format(blueprint), blueprint

    def init_app(self, app):
        self._flask_app = app

        # Config variables
        self._flask_app.config.setdefault('ROUTER_BUILDER_URL_PREFIX', None)
        self._flask_app.config.setdefault('ROUTER_BUILDER_IGNORE_LIST', [])

        self.ignore_list += self._flask_app.config['ROUTER_BUILDER_IGNORE_LIST']

        apps_list = [p for p in os.listdir(self._blueprints_package) if os.path.isdir(p) and p not in self.ignore_list]        
        
        if self._blueprints_package:
            #: List all blueprints in the application blueprints package and return a list of tuples with (url, module_name)
            self._blueprints = [self._format_route(module_name, self._blueprints_package) for _, module_name, _ in
                                pkgutil.iter_modules([self._blueprints_package])]
        else:
            # List all blueprints in the same level of core package.
             self._blueprints = [self._format_route(module_name, self._blueprints_package) for module_name in apps_list]

        for module_namespace, module_name in self._blueprints:
            blueprint = __import__(module_namespace, globals(), locals(), [module_name], 0)
            if self._flask_app.config['ROUTER_BUILDER_URL_PREFIX'] is not None:
                self._flask_app.register_blueprint(getattr(blueprint, module_name),
                                                   url_prefix='/{0}/{1}'.format(
                                                       self._flask_app.config['ROUTER_BUILDER_URL_PREFIX'], module_name))
            else:
                self._flask_app.register_blueprint(getattr(blueprint, module_name),url_prefix='/{0}'.format(module_name))