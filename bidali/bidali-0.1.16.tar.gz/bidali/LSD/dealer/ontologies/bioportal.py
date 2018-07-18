# -*- coding: utf-8 -*-
"""Ontologies from BioPortal

Reference: https://bioportal.bioontology.org/
"""
from bidali import LSD
from bidali.config import secrets
from bidali.LSD import retrieveSources,cacheableTable,processedDataStorage,datadir
import os, gzip, pandas as pd
from io import TextIOWrapper, StringIO
import urllib.request, urllib.error, urllib.parse
import json

REST_URL = "http://data.bioontology.org"

def list_ontologies(printout=True):
    import os
    from pprint import pprint
    
    API_KEY = secrets.getsecret('bioportal') #need to register -> then https://bioportal.bioontology.org/account API key
    
    def get_json(url):
        opener = urllib.request.build_opener()
        opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
        return json.loads(opener.open(url).read())
    
    # Get the available resources
    resources = get_json(REST_URL + "/")
    
    # Get the ontologies from the `ontologies` link
    ontologies = get_json(resources["links"]["ontologies"])
    
    # Get the name and ontology id from the returned list
    ontology_output = []
    for ontology in ontologies:
        ontology_output.append(f"{ontology['name']}\n{ontology['@id']}\n")
    
    # Print the first ontology in the list
    #pprint(ontologies[0])
    
    # Print/return the names and ids
    if printout:
        print("\n\n")
        for ont in ontology_output:
            print(ont)
    else: return ontology_output

def get_labels(acronym):
    """
    Reference:
        https://github.com/ncbo/ncbo_rest_sample_code/blob/master/python/python3/get_labels.py

    Example:
        get_labels('BRO')
    """
    API_KEY = secrets.getsecret('bioportal') #need to register -> then https://bioportal.bioontology.org/account API key    
    
    def get_json(url):
        opener = urllib.request.build_opener()
        opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
        return json.loads(opener.open(url).read())
    
    # Get all ontologies from the REST service and parse the JSON
    ontologies = get_json(REST_URL+"/ontologies")
    
    # Iterate looking for ontology with acronym BRO
    bro = None
    for ontology in ontologies:
        if ontology["acronym"] == acronym:
            bro = ontology
    
    labels = []
    
    # Using the hypermedia link called `classes`, get the first page
    page = get_json(bro["links"]["classes"])
    
    # Iterate over the available pages adding labels from all classes
    # When we hit the last page, the while loop will exit
    next_page = page
    while next_page:
        next_page = page["links"]["nextPage"]
        for bro_class in page["collection"]:
            labels.append(bro_class["prefLabel"])
        if next_page:
            page = get_json(next_page)
    
    # Output the labels
    for label in labels:
        print(label)
    
