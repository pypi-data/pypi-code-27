#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: graph.py
Author: zach.lamberty
Created: 2018-08-01

Description:
    common graph utilities

Usage:
    >>> import eri.graph

"""

from . import logging as _logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

_LOGGER = _logging.getLogger(__name__)


# ----------------------------- #
#   network to neo4j            #
# ----------------------------- #

class EriGraphError(Exception):
    def __init__(self, msg, *args, **kwargs):
        _LOGGER.error(msg)
        super().__init__(*args, **kwargs)


# wanted the logger and the class-specific error to perform this conditional
# import
try:
    from neo4j.v1 import (
        GraphDatabase as _GraphDatabase,
        basic_auth as _basic_auth
    )
except ImportError:
    _LOGGER.debug("to install the neo4j package run")
    _LOGGER.debug(">>> pip install -U neo4j-driver")
    _LOGGER.debug(
        "neo4j-driver is not available on the conda default channel at this time"
    )
    _LOGGER.debug(
        "the project homepage is located at "
        "https://github.com/neo4j/neo4j-python-driver/wiki"
    )
    raise EriGraphError(
        "unable to load the neo4j driver python package; please install it"
    )



def _verify_constraints(session, constraints):
    """verify existence of `constraints` in the `session`'s database.

    iterate through a collection of (`NodeLabel`, `prop`) pairs and ensure
    that a uniqueness constraint exists for that pair. specifically, this will
    execute the `cypher` query

        `create constraint on (n:NodeLabel) assert n.prop is unique`

    for every `NodeLabel`, `prop` pair.

    args:
        session (neo4j.v1.api.Session): an active neo4j driver session
        constraints (list): an iterable of (`NodeLabel`, `prop`) pairs for
            which you would like to create uniqueness constraints

    returns:
        None

    raises:
        None

    """
    for (label, prop) in required_constraints:
        session.run(
            'create constraint on (n:{}) assert n.{} is unique'.format(
                label, prop
            )
        )


def _make_node_qry(node_name, properties):
    node_label = properties.get('label')
    if node_label is None:
        raise EriGraphError("all nodes must have labels to be added to neo4j")

    merge_str = 'MERGE (n:{label} {{name: "{name}"}})'.format(
        label=node_label,
        name=node_name,
    )

    set_str = []
    for (attr, val) in properties.items():
        if attr != 'label':
            set_str.append('n.{} = {}'.format(attr, json.dumps(val)))
    set_str = ', '.join(set_str)

    if set_str:
        on_create_str = 'on create set {}'.format(set_str)
    else:
        on_create_str = ''

    return_str = "return id(n)"

    qry = ' '.join([merge_str, on_create_str, return_str])

    return qry


def _make_edge_qry(src, src_label, dst, dst_label, properties):
    edge_type = properties.get('_type')
    if edge_type is None:
        raise EriGraphError(
            "all edges must have a type (key is \"_type\") to be added to neo4j"
        )

    nodefmt = '({alias}:{label} {{name: "{name}"}})'
    src_node_str = nodefmt.format(alias='src', label=src_label, name=src)
    dst_node_str = nodefmt.format(alias='dst', label=dst_label, name=dst)

    merge_str = "MATCH {src:} MATCH {dst:} MERGE (src)-[e:{etype}]->(dst)"
    merge_str = merge_str.format(
        src=src_node_str,
        etype=edge_type,
        dst=dst_node_str,
    )

    set_str = []
    for (attr, val) in properties.items():
        if attr != '_type':
            set_str.append('e.{} = {}'.format(attr, json.dumps(val)))
    set_str = ', '.join(set_str)

    if set_str:
        on_create_str = 'on create set {}'.format(set_str)
    else:
        on_create_str = ''

    return_str = "return id(e)"

    qry = ' '.join([merge_str, on_create_str, return_str])

    return qry


def nx_to_neo(graph, dbconf, constraints=None):
    """persist a networkx graph to a neo4j database

    there are some assumptions about the passed networkx graph being made here:

        1. all graph `node`s must have a `label` attribute (used as the node
            label in neo4j)
        2. all graph `edge`s must have a `_type` attribute (used as the edge
            label in neo4j)
        3. all graph `edge`s are directed (this is because all neo edges are
            directed). an undirected `networkx` graph will be converted into a
            directed neo graph. the `graph.edges` method will return tuples that
            are assumed to be `(source, destination)` pairs

    for short-term projects / poc, consider using the neo4j sandbox environments
    [here](https://neo4j.com/sandbox-v2/). this will make spinning up
    significantly easier as it allows you to skip the infrastructure phase

    args:
        graph (nx.DiGraph): category graph
        dbconf (dict): dictionary of connection information for the neo4j
            datbase. must contain the keys `ip`, `port`, `user`, and `pw`.
            `port` is the *bolt* port, not the hhtp port.
        constraints (list): a list of constraint tuples used to verify that
            desired constraints exist in the database before creating nodes and
            edges. see the neighboring `verify_constraints` function for further
            documentation. if `None` is passed, no constraints will be created
            in the neo database. (default: `None`)

    """
    url = 'bolt://{}:{}'.format(dbconf["ip"], dbconf["port"])
    auth = _basic_auth(dbconf["user"], dbconf["pw"])
    with _GraphDatabase.driver(url, auth=auth) as driver:
        with driver.session() as session:
            _verify_constraints(session)

            # handle nodes first, then handle edges
            _LOGGER.info('updating nodes in neo4j')
            for i, (node_name, properties) in enumerate(graph.nodes(data=True)):
                qry = _make_node_qry(node_name, properties)
                _LOGGER.debug(qry)
                res = session.run(qry)

            _LOGGER.info('updating relationships in neo4j')
            for i, (src, dst, properties) in enumerate(graph.edges(data=True)):
                src_label = graph.node[src]['label']
                dst_label = graph.node[dst]['label']
                qry = _make_edge_qry(src, src_label, dst, dst_label, properties)
                _LOGGER.debug(qry)
                res = session.run(qry)
