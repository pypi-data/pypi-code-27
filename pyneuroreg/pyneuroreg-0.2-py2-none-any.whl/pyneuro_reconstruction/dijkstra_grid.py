import pyneuro_io.amiraparsing as ap
import numpy as np
import time
import math



def euclidean_distance(pt1, pt2):
    x_diff = pt2[0] - pt1[0]
    y_diff = pt2[1] - pt1[1]
    z_diff = pt2[2] - pt1[2]
    return math.sqrt(x_diff*x_diff + y_diff*y_diff + z_diff*z_diff)


import sys

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxint
        # Mark all nodes unvisited        
        self.visited = False  
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' with adjacent: ' + str([x.id for x in self.adjacent])

class Graph:
    ## graph_dict -> vertex (int) : neighboring nodes (int)
    ## vert_dict -> vertex_id : vertex instance (which includes neighboring nodes) 
    
    def __init__(self, graph_dict = None, ptAr = None):
        if graph_dict == None and ptAr == None:
            self.vert_dict = {}
            self.num_vertices = 0
            
        else:
            self.graph_dict = graph_dict
            self.ptAr = ptAr
            self.vert_dict = {}
            self.num_vertices = 0
#             for from_vertex in self.vert_dict.keys():
#                 for to_vertex in self.vert_dict[from_vertex]:
#                     self.add_vertex(from_vertex)
#                     self.add_vertex(to_vertex)

            for from_vertex in self.graph_dict.keys():
#                 print type(from_vertex)
#                 print type(self.vert_dict.keys()[0])
#                 print type(self.vert_dict.values()[0])
                for to_vertex in self.graph_dict[from_vertex]:
                    if from_vertex not in self.vert_dict.keys():
                        self.add_vertex(from_vertex)
                        #print self.vert_dict.keys()
                    if to_vertex not in self.vert_dict.keys():
                        self.add_vertex(to_vertex)
                    cost = euclidean_distance(self.ptAr[from_vertex], self.ptAr[to_vertex])
#                     print self.vert_dict[from_vertex]
#                     print self.vert_dict[to_vertex]
#                     print cost
                    self.vert_dict[from_vertex].add_neighbor(self.vert_dict[to_vertex], cost)

                    
    def __iter__(self):
        return iter(self.vert_dict.values())

    def euclidean_distance(pt1, pt2):
        x_diff = pt2[0] - pt1[0]
        y_diff = pt2[1] - pt1[1]
        z_diff = pt2[2] - pt1[2]
        return math.sqrt(x_diff*x_diff + y_diff*y_diff + z_diff*z_diff)

    def get_vert_dict(self):
        return self.vert_dict
    
    def __str__(self):
        return str(self.vert_dict)
    
    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return


import dask
import heapq

#@dask.delayed
def dijkstra(node_dict, ptAr, start_vertex):
    aGraph = Graph(node_dict, ptAr)
    print " Starting Dijkstra on vertex: " + str(start_vertex) + " "
    # Set the distance for the start node to zero 
    start = aGraph.get_vertex(start_vertex)
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(),v) for v in aGraph]
#     print "unvisited queue: "
#     #print [t[1] for t in unvisited_queue]
#     for t in unvisited_queue:
#         print t[1]
#     print "End of the queue"
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue): # as long as there's an element in the list 
        # Pops a vertex with the smallest distance 
        uv = heapq.heappop(unvisited_queue)
        #print uv 
        current = uv[1]
        current.set_visited()

        #for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)
            
            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                #print 'updated : current = %s next = %s new_dist = %s' \
                        #%(current.get_id(), next.get_id(), next.get_distance())
            #else:
                #print 'not updated : current = %s next = %s new_dist = %s' \
                        #%(current.get_id(), next.get_id(), next.get_distance())

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
        
#         print "unvisited queue: "
#         for t in unvisited_queue:
#             print t[1]
#         print "End of the queue"
        
        heapq.heapify(unvisited_queue)
#     path = [target.get_id()]
#     shortest(target, path)
#     return path
    
    print " Dijkstra is done on vertex: " + str(start_vertex) +" "
    graph_vert_dict = aGraph.get_vert_dict()
    
    distance_matrix = []
    
    for target_vertex in range(len(graph_vert_dict)):
        distance_matrix.append(graph_vert_dict[target_vertex].get_distance())
        
    return distance_matrix




