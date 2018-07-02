import os
import sys
import inspect
from functools import wraps, partial

from werkzeug.contrib.cache import SimpleCache
from werkzeug.local import LocalProxy, LocalStack
from flask import current_app, json, request as flask_request, _app_ctx_stack
from . import logger


def find_ask():
    """
    Find our instance of Rak, navigating Local's and possible blueprints.
    Note: This only supports returning a reference to the first instance
    of Rak found.
    """
    if hasattr(current_app, 'rak'):
        return getattr(current_app, 'rak')
    else:
        if hasattr(current_app, 'blueprints'):
            blueprints = getattr(current_app, 'blueprints')
            for blueprint_name in blueprints:
                if hasattr(blueprints[blueprint_name], 'rak'):
                    return getattr(blueprints[blueprint_name], 'rak')


def dbgdump(obj, default=None, cls=None):
    if current_app.config.get('RAK_PRETTY_DEBUG_LOGS', False):
        indent = 2
    else:
        indent = None
    msg = json.dumps(obj, indent=indent, default=default, cls=cls)
    logger.debug(msg)
    print msg


request = LocalProxy(lambda: find_ask().request)
session = LocalProxy(lambda: find_ask().session)
version = LocalProxy(lambda: find_ask().version)
context = LocalProxy(lambda: find_ask().context)

from . import models


class RAK(object):
    def __init__(self, app=None, route=None, blueprint=None):
        self.app = app
        self._route = route
        self._intent_view_funcs = {}
        self._launch_view_func = None
        self._default_intent_view_func = None

        if app is not None:
            self.init_app(app)
        elif blueprint is not None:
            self.init_blueprint(blueprint)

    def init_app(self, app):
        """Initializes Ask app by setting configuration variables and maps RAK route to a flask view.
        The RAK instance is given the following configuration variables by calling on Flask's configuration:

        """
        if self._route is None:
            raise TypeError(
                "route is a required argument when app is not None")

        app.rak = self
        app.add_url_rule(
            self._route, view_func=self._flask_view_func, methods=['POST'])

    def init_blueprint(self, blueprint):
        """Initialize a Flask Blueprint, similar to init_app, but without the access
        to the application config.
        Keyword Arguments:
            blueprint {Flask Blueprint} -- Flask Blueprint instance to initialize (Default: {None})
        """
        if self._route is not None:
            raise TypeError("route cannot be set when using blueprints!")

        blueprint.rak = self
        blueprint.add_url_rule(
            "", view_func=self._flask_view_func, methods=['POST'])

    @property
    def session(self):
        return getattr(_app_ctx_stack.top, '_rak_session', models._Field())

    @session.setter
    def session(self, value):
        _app_ctx_stack.top._rak_session = value

    @property
    def version(self):
        return getattr(_app_ctx_stack.top, '_rak_version', None)

    @version.setter
    def version(self, value):
        _app_ctx_stack.top._rak_version = value

    @property
    def context(self):
        return getattr(_app_ctx_stack.top, '_ask_context', None)

    @context.setter
    def context(self, value):
        _app_ctx_stack.top._ask_context = value

    def launch(self, f):
        """Decorator maps a view function as the endpoint for an LaunchRequest and starts the app.
        @ask.launch
        def launched():
            return question('Welcome to Foo')
        The wrapped function is registered as the launch view function and renders the response
        for requests to the Launch URL.
        Arguments:
            f {function} -- Launch view function
        """
        self._launch_view_func = f

        @wraps(f)
        def wrapper(*args, **kw):
            self._flask_view_func(*args, **kw)
        return f

    def intent(self, intent_name):
        """Decorator routes an Rogo IntentRequest.
        Functions decorated as an intent are registered as the view function for the Intent's URL,
        and provide the backend responses to give your Skill its functionality.
        @ask.intent('WeatherIntent')
        def weather(city):
            return statement('I predict great weather for {}'.format(city))
        Arguments:
            intent_name {str} -- Name of the intent request to be mapped to the decorated function
        """
        def decorator(f):
            self._intent_view_funcs[intent_name] = f

            @wraps(f)
            def wrapper(*args, **kw):
                self._flask_view_func(*args, **kw)
            return f
        return decorator

    def default_intent(self, f):
        """Decorator routes any Rogo IntentRequest that is not matched by any existing intent routing."""
        self._default_intent_view_func = f

        @wraps(f)
        def wrapper(*args, **kw):
            self._flask_view_func(*args, **kw)
        return f

    def _rogo_request(self):
        raw_body = flask_request.data
        rogo_request_payload = json.loads(raw_body)

        return rogo_request_payload

    def _flask_view_func(self, *args, **kwargs):
        rak_payload = self._rogo_request()
        dbgdump(rak_payload)
        request_body = models._Field(rak_payload)
        print request_body

        self.version = request_body.version
        self.context = getattr(request_body, 'context', models._Field())
        self.session = getattr(request_body, 'session', self.session) # to keep old session.attributes through AudioRequests
 
        if not self.session:
            self.session = models._Field()
        if not self.session.attributes:
            self.session.attributes = models._Field()
    
        if context.type == 'LaunchRequest' and self._launch_view_func:
            result = self._launch_view_func(request_body)
        elif context.type == 'IntentRequest' and self._intent_view_funcs:
            result = self._map_intent_to_view_func(self.context.intent)()

        if result is not None:
            if isinstance(result, models._Response):
                return result.render_response()
            return result
        return "", 400

    def _map_intent_to_view_func(self, intent):
        """Provides appropiate parameters to the intent functions."""
        if intent.label in self._intent_view_funcs:
            view_func = self._intent_view_funcs[intent.label]
        elif self._default_intent_view_func is not None:
            view_func = self._default_intent_view_func
        else:
            raise NotImplementedError('Intent "{}" not found and no default intent specified.'.format(intent.name))

        argspec = inspect.getargspec(view_func)
        arg_names = argspec.args
        arg_values = self._map_params_to_view_args(intent.label, arg_names)

        return partial(view_func, *arg_values)
    
    def _map_params_to_view_args(self, view_name, arg_names):
        arg_values = []

        request_data = {}

        entities = getattr(self.context, 'entities', None)
        if entities is not None:
            for entity in entities:
                request_data[entity['entity']] = entity['value']

        else:
            for param_name in self.context:
                request_data[param_name] = getattr(self.context, param_name, None)
        
        for arg_name in arg_names:
            arg_value = request_data.get(arg_name)
            arg_values.append(arg_value)
        return arg_values