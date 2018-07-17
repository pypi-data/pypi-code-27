import requests
import json
from collections import defaultdict
from rdflib import URIRef
from IPython import embed

def parse_to_uri(thing):
    if isinstance(thing, URIRef):
        return thing
    else:
        ns = thing.get('Namespace')
        if len(ns) > 0:
            ns += '#'
        return URIRef(ns + thing.get('Value',''))
        

class Row(object):
    def __init__(self, variables):
        self.values = variables.copy()
        for k,v in variables.items():
            key = k.lstrip('?')
            value = parse_to_uri(v)
            self.values[k] = value
            setattr(self, key, value)

    def __eq__(self, other):
        return sorted(self.values.items()) == sorted(other.values.items())

    def __hash__(self):
        return hash(tuple(sorted(self.values.items())))

    def get(self, values):
        return Row({k: v for k,v in self.values.items() if k in values})

    def pop(self, values):
        return Row({k: v for k,v in self.values.items() if k not in values})

    def __repr__(self):
        return '<{0}>'.format(','.join(['{0}={1}'.format(k,v) for k,v in self.values.items()]))

class Result(object):
    def __init__(self, obj, groupby=None):
        self.count = obj['Count']
        self.elapsed = obj['Elapsed']
        self.rows = []
        if obj['Rows'] is None:
            return
        for row in obj['Rows']:
            self.rows.append(Row(row))
        if groupby is not None:
            self.rows = self.groupby(groupby)

    def groupby(self, order):
        d = defaultdict(list)
        o_idx = 0
        for row in self.rows:
            key = order[o_idx]
            d[row.get(key)].append(row.pop(key))
        return dict(d)

class Client():
    def __init__(self, url="http://localhost:47808"):
        self.url = url

    def query(self, query, timeout=60, groupby=None):
        resp = requests.get(self.url+'/api/query', data=query, timeout=timeout)
        if not resp.ok:
            raise Exception("Query to {0} failed ({1})".format(self.url, resp.reason))
        return Result(resp.json(), groupby=groupby)

    def search(self, terms, number=500, timeout=60):
        terms = terms if isinstance(terms, str) else ' '.join(terms)
        resp = requests.get(self.url+'/api/search', data=json.dumps({'Query': terms, 'Number': number}), timeout=timeout)
        if not resp.ok:
            raise Exception("Search to {0} failed ({1})".format(self.url, resp.reason))
        return resp.json()
