from django.conf import settings
from django.core.management.base import BaseCommand
from waitress import serve

from django.core.wsgi import get_wsgi_application


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('host', nargs='?', default=None)
        parser.add_argument('port', nargs='?', type=int, default=None)
        parser.add_argument('--unix', dest='unix', default=None)

    def handle(self, *args, **options):
        application = get_wsgi_application()

        if options['unix'] is not None:
            serve(application, unix_socket=options['unix'])
        else:
            host = options['host']
            if host is None:
                host = getattr(settings, 'WAITRESS_HOST', 'localhost')
            port = options['port']
            if port is None:
                port = getattr(settings, 'WAITRESS_PORT', 8000)

            serve(application, host=host, port=port)
