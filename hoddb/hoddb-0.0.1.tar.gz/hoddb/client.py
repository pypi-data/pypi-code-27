import requests
import json
from rdflib import URIRef

class Row(object):
    def __init__(self, variables):
        self.values = variables
        for k,v in variables.items():
            key = k.lstrip('?')
            ns = v.get('Namespace')
            if len(ns) > 0:
                ns += '#'
            value = URIRef(ns + v.get('Value',''))
            self.values[k] = value
            setattr(self, key, value)

    def __repr__(self):
        return '<{0}>'.format(','.join(['{0}={1}'.format(k,v) for k,v in self.values.items()]))

class Result(object):
    def __init__(self, obj):
        self.count = obj['Count']
        self.elapsed = obj['Elapsed']
        self.rows = []
        for row in obj['Rows']:
            self.rows.append(Row(row))
        pass

class Client():
    def __init__(self, url="http://localhost:47808"):
        self.url = url

    def query(self, query, timeout=60):
        resp = requests.get(self.url+'/api/query', data=query, timeout=timeout)
        if not resp.ok:
            raise Exception("Query to {0} failed ({1})".format(self.url, resp.reason))
        return Result(resp.json())

    def search(self, terms, number=500, timeout=60):
        terms = terms if isinstance(terms, str) else ' '.join(terms)
        resp = requests.get(self.url+'/api/search', data=json.dumps({'Query': terms, 'Number': number}), timeout=timeout)
        if not resp.ok:
            raise Exception("Search to {0} failed ({1})".format(self.url, resp.reason))
        return resp.json()
