#!/usr/bin/env python
from collections import namedtuple as nt

# As long as it has a name addr and port attribute, you're good.
Host = nt('Host', 'name addr port')

class Cluster(object):

    def __init__(self, hosts=None):
        """
        Initialize a cluster. Extensible

        @kwarg hosts: A list of objects with (name,addr,port) attributes
        """
        if hosts is None:
            self.hosts = []
        else:
            self.hosts = hosts

SAMPLE_CLUSTER = Cluster(hosts=[
    Host("ui", "1.0.0.0", 22),
    Host("other_ui", "1.0.0.1", 2222),
    Host("new_ui", "ui.example.com", 22),
])

