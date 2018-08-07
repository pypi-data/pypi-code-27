#!/usr/bin/env python

import click

from gtsrvd import app


@click.command()
@click.option("--domain", default="example.com", help="Target domain")
@click.option("--subdomain", default="test1", help="Target subdomain")
@click.option("--port", default=80, help="Target port to proxy to")
def create(domain, subdomain, port):
    """ Create proxy to localhost on port. Will add dns record to domain. """
    app.create(domain, subdomain, int(port))


@click.command()
@click.option("--domain", default="example.com", help="Target domain")
@click.option("--subdomain", default="test1", help="Target subdomain")
@click.option("--port", default=80, help="Target port to proxy to")
def delete(domain, subdomain, port):
    """ Delete proxy to localhost on port. Will remove dns record from domain. """
    app.delete(domain, subdomain, int(port))
