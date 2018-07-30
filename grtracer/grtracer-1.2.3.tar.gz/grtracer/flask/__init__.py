from flask import request

from jaeger_client import Config
from flask_opentracing import FlaskTracer
from opentracing_instrumentation.client_hooks import install_patches
from opentracing_instrumentation.request_context import RequestContextManager


class GrTFlaskMiddleware(object):
    def __init__(self, app, name, host='localhost', rate=0, header='GROFERS_TRACE_ID', patches=[]):
        self.cfg = Config(
            config={
                'sampler': {'type': 'const', 'param': rate},
                'local_agent': {'reporting_host': host},
                'trace_id_header': header
            },
            service_name=name
        )
        self.app = app
        self.initialized = False

        app.before_request(self._start_trace)
        app.after_request(self._end_trace)

        permitted_patches = [
           'mysqldb',
           'psycopg2',
           'strict_redis',
           'sqlalchemy',
           'tornado_http',
           'urllib',
           'urllib2',
           'requests',
        ]
        final_patches = []
        for patch in patches:
            if not patch in permitted_patches:
                raise ValueError('{} is not a valid patch'.format(patch))
            else:
                final_patches.append(
                    'opentracing_instrumentation.client_hooks.{}.install_patches'.format(patch))
        install_patches(final_patches)

    def _start_trace(self):
        if not self.initialized:
            self.tracer = self.cfg.initialize_tracer()
            self.ftracer = FlaskTracer(self.tracer, False, self.app)
            self.initialized = True
        span = self.ftracer.get_span(request)
        if span is None:
            span = self.tracer.start_span(request.endpoint)
        mgr = RequestContextManager(span=span)
        mgr.__enter__()

        request.span = span
        request.mgr = mgr

    def _end_trace(self, response):
        request.span.finish()
        request.mgr.__exit__()
        return response
