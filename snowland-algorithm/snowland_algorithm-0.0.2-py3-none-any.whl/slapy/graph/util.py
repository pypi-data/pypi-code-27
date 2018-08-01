#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site:
# @file: _dijkstra.py
# @time: 2018/5/30 17:34
# @Software: PyCharm

"""
    本代码从源自开源项目algorithms
    https://github.com/keon/algorithms
    链接为
    https://github.com/keon/algorithms/blob/master/graph/graph.py
"""

"""
These are classes to represent a Graph and its elements.
It can be shared across graph algorithms.
"""


class Node(object):
    def __init__(self, n):
        if isinstance(n, (str, )):
            self._name = n
        elif isinstance(n, (Node,)):
            self._name = n.name
        else:
            self._name = str(n)

    def __str__(self):
        return self.name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        if isinstance(n, (str, )):
            self._name = n
        elif isinstance(n, (Node,)):
            self._name = n
        else:
            self._name = str(n)

    def __eq__(self, obj):
        return self._name == obj.name

    def __repr__(self):
        return self._name

    def __hash__(self):
        return hash(self.name)

    def __ne__(self, obj):
        return self._name != obj.name

    def __lt__(self, obj):
        return self._name < obj.name

    def __le__(self, obj):
        return self._name <= obj.name

    def __gt__(self, obj):
        return self._name > obj.name

    def __ge__(self, obj):
        return self._name >= obj.name

    def __bool__(self):
        return self._name


class DirectedEdge(object):
    def __init__(self, node_from, node_to, weight=1):
        self.nf = Node(node_from)
        self.nt = Node(node_to)
        self.weight = weight

    def __str__(self):
        return '({0} -> {1}, {2})'.format(self.nf, self.nt, self.weight)


class DirectedGraph(object):
    def __init__(self, nodes=None, edges=None, load_dict={}):
        if load_dict:
            self.graph = load_dict
            self.nodes = [Node(k) for k, _ in enumerate(load_dict)]
            self.edges = [[DirectedEdge(k, item_k, item_w) for item_k, item_w in v] for k, v in enumerate(load_dict)]
        else:
            self.nodes = nodes if nodes else []
            self.edges = edges if edges else []
            graph = {}
            for node in nodes:
                graph[node.name] = {}

            for edge in edges:
                graph[edge.nf][edge.nt] = edge.weight
            self.graph = graph

    def add_node(self, node=None, node_name=None):
        node_name = node.name if node else node_name
        try:
            return self.nodes[self.nodes.index(node_name)]
        except ValueError:
            node = Node(node_name)
            self.nodes.append(node)
            self.graph[node.name] = {}
            return node

    def add_edge(self, node_name_from=None, node_name_to=None, weight=1, node_from=None, node_to=None):
        if node_name_from and node_name_to:
            node_from = self.nodes[self.nodes.index(node_name_from)]
            node_to = self.nodes[self.nodes.index(node_name_to)]
        edge = DirectedEdge(node_from, node_to, weight)
        self.edges.append(edge)
        self.graph[node_from.name][node_to.name] = weight
        return edge


class Graph(object):
    def __init__(self, nodes=None, edges=None, load_dict={}):
        if load_dict:
            self.graph = load_dict
            self.nodes = [Node(k) for k, _ in enumerate(load_dict)]
            self.edges = [[DirectedEdge(k, item_k, item_w) for item_k, item_w in v] for k, v in enumerate(load_dict)]
        else:
            self.nodes = nodes if nodes else []
            self.edges = edges if edges else []
            graph = {}
            for node in nodes:
                graph[node.name] = {}

            for edge in edges:
                self.add_edge(edge)

    def add_edge(self, edge=None, u=None, v=None, weight=1, u_name=None, v_name=None):
        if edge:
            u, v, weight = edge.nf, edge.nt, edge.weight
        u_name = u.name if u else u_name
        v_name = v.name if v else v_name
        if u_name in self.graph.keys():
            self.graph[u_name][v_name] = weight
            edge = DirectedEdge(Node(u_name), Node(v_name), weight)
        elif v.name in self.graph.keys():
            self.graph[v_name][u_name] = weight
            edge = DirectedEdge(Node(v_name), Node(u_name), weight)
        else:
            self.graph[u_name] = {}
            self.graph[u_name][v_name] = weight
            edge = DirectedEdge(Node(u_name), Node(v_name), weight)
        self.edges.append(edge)
        return edge

    def add_node(self, node=None, node_name=None):
        node_name = node.name if node else node_name
        try:
            return self.nodes[self.nodes.index(node_name)]
        except ValueError:
            node = Node(node_name)
            self.nodes.append(node)
            self.graph[node.name] = {}
            return node
