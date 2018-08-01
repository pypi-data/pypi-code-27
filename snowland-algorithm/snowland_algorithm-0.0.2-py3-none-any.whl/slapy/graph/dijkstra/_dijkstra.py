#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: _dijkstra.py
# @time: 2018/5/30 17:34
# @Software: PyCharm

import numpy as np
npa = np.array
npm = np.mat
from scipy.spatial import distance
def dijkstra(s ,node=0):
    s = npa(s)
    graph = s
    vertices = s.shape[0]
    dist = np.ones(vertices) * np.inf
    dist[node] = 0
    min_dist_set = np.zeros(vertices)

    for count in range(vertices):

        # minimum distance vertex that is not processed
        u = s[dist, min_dist_set]

        # put minimum distance vertex in shortest tree
        min_dist_set[u] = True

        # Update dist value of the adjacent vertices
        for v in range(vertices):
            if graph[u][v] > 0 and min_dist_set[v] == False and dist[v] > dist[u] + self.graph[u][v]:
                dist[v] = dist[u] + graph[u][v]

    return dist

if __name__ == '__main__':
    a = npm('[0,2,6,4;'
            '100000,0,3,100000;'
            '7,100000,0,1;'
            '5,100000,12,0'
            ']')
    dist = dijkstra(a, node=1)
    print(dist)