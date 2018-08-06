#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""URL shortening service to be used in a microservices environment.

"""

# Standard
import base64
import hashlib
import logging
import logging.config
import logging.handlers
import argparse

# Third party
import validators
import tornado.web
import tornado.ioloop
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Local
from .settings import *
from .models import URL, Base

# Logging
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

# Cli arguments to override default settings.
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', help='Port used for this service',
                    type=int, default=HTTP_PORT)

parser.add_argument('-d', '--database', help='Database to use',
                    type=str, default=DATABASE)

# TODO: Added Fluend to the settigs
# parser.add_argument('--logging-host', help='Fluentd service host to log to',
#                     type=str)
# parser.add_argument('--logging-port', help='Fluentd service port to log to',
#                     type=str)
args = parser.parse_args()


class InvalidUrlException(tornado.web.HTTPError):
    pass


class PrometheusHandler(tornado.web.RequestHandler):
    """Microservice instrumentation endpoint with Prometheus
    If this service is part of a microservices architecture it would need
    an instrumentation endpoint. See http://microservices.io for
    architecture info
    """

    def get(self):
        # TODO: Export metrics
        pass


class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        """Preparing database connection"""
        self.engine = create_engine(args.database)
        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = self.engine

        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def valid(self, url):
        """Validating the url prior to saving in the DB.

        :param url: String
        :return: Boolean
        """
        if validators.url(url):
            return True
        return False

    def create(self, url):
        """Retrieves or creates URL records

        :param url: Long url
        :return: url record from the database
        """
        record = self.session.query(URL).filter(URL.url == url).first()
        if not record:
            # Create record in DB
            record = URL(url=url)
            self.session.add(record)
            self.session.commit()

        return record

    def retrieve(self, key):
        """Retrieves a record from the DB

        :param key: key
        :return: url record from the database
        """
        id = int(base64.b64decode(key))
        return self.session.query(URL).filter(URL.id == id).first()

    def remove(self, key):
        """Deletes a record from the DB

        :param key: key
        :return: url record from the database
        """
        id = int(base64.b64decode(key))
        record = self.session.query(URL).filter(URL.id == id).first()
        if record:
            # Delete record from DB
            self.session.delete(record)
            self.session.commit()
            return True
        return False


class ShortHandler(BaseHandler):
    """Endpoint handler for creating short urls and redirecting."""

    def delete(self, key):
        """Deletes url record"""
        if self.remove(key):
            self.write('Successfully deleted url')
        else:
            raise InvalidUrlException(reason='Not Found', status_code=404)

    def post(self, *pargs):
        """Creates a short url from a long url."""
        if self.valid(self.request.body.decode("utf-8")):
            record = self.create(self.request.body)
            url = '{}://{}/{}'.format(self.request.protocol,
                                      self.request.host,
                                      record.key())
            self.write(url)
        else:
            raise InvalidUrlException(reason='Invalid URL', status_code=400)

    def get(self, key):
        """Retrieve and redirect to long url in DB.

        :param url: Short url
        :return: Redirects or response message.
        """
        if key:
            # Get the url record from the urls table
            record = self.retrieve(key)
            if record:
                self.redirect(record.url)
            else:
                raise InvalidUrlException(reason='Not Found', status_code=404)

        else:
            self.write('curl -X POST -H "Content-Type: text/plain" --data '
                       '"http://www.example.com/this-is-the-longest-url-in'
                       '-the-world" {}://{}'.format(self.request.protocol,
                                      self.request.host))


def service():
    svc = tornado.web.Application([
        # Instrumentation endpoint
        # (r"/metric", PrometheusHandler),

        (r"/(.*)", ShortHandler),
    ])
    svc.listen(args.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    service()
