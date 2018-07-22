from pyneuro_io import amiraparsing as ap
import numpy as np
import time
import math
# import dask
import heapq
import sys
from tqdm import tqdm_notebook as tqdm # if you want to run it in jupyter notebook

'''
Written by Peter Park 

'''


################################################################################################
## Usage example 

# start_t = time.time()
# test1 = ap.amiraParsingSurface(input2)
# ptAr = ap.convertToFloat(test1[0])
# tris = ap.convertToInt(test1[1])
# end_t = time.time()
# print "Reading the data took: " + str(end_t-start_t)

# nodeList = []
# for tri in tris:
#     tri = sorted(tri)
#     #since the triangle index starts from 1, so need to re-adjust it to start from 0 
#     nodeList.append((tri[0]-1, tri[1]-1))
#     nodeList.append((tri[1]-1, tri[0]-1))
#     nodeList.append((tri[1]-1, tri[2]-1))
#     nodeList.append((tri[2]-1, tri[1]-1))
#     nodeList.append((tri[0]-1, tri[2]-1))
#     nodeList.append((tri[2]-1, tri[0]-1))
# nodes = list(set(nodeList))
# nodes.sort(key=lambda tup: tup[0])
# node_dict = {}
# for node in nodes:  
#     node_dict.setdefault(node[0], []).append(node[1])

################################################################################################


def generate_nodeDict_file(file):
    surface_parsed = ap.amiraParsingSurface(file)
    # ptAr = ap.convertToFloat(surface_parsed[0])
    tris = ap.convertToInt(surface_parsed[1])

    nodeList = []
    for tri in tris:
        tri = sorted(tri)
        #since the triangle index starts from 1, so need to re-adjust it to start from 0 
        nodeList.append((tri[0]-1, tri[1]-1))
        nodeList.append((tri[1]-1, tri[0]-1))
        nodeList.append((tri[1]-1, tri[2]-1))
        nodeList.append((tri[2]-1, tri[1]-1))
        nodeList.append((tri[0]-1, tri[2]-1))
        nodeList.append((tri[2]-1, tri[0]-1))
    nodes = list(set(nodeList))
    nodes.sort(key=lambda tup: tup[0])
    node_dict = {}
    for node in nodes:  
        node_dict.setdefault(node[0], []).append(node[1])

    return node_dict

## Shows which node is connected to which other nodes
def generate_nodeDict(tris):

    nodeList = []
    for tri in tris:
        tri = sorted(tri)
        #since the triangle index starts from 1, so need to re-adjust it to start from 0 
        nodeList.append((tri[0], tri[1]))
        nodeList.append((tri[1], tri[0]))
        nodeList.append((tri[1], tri[2]))
        nodeList.append((tri[2], tri[1]))
        nodeList.append((tri[0], tri[2]))
        nodeList.append((tri[2], tri[0]))

    nodes = list(set(nodeList))
    nodes.sort(key=lambda tup: tup[0])
    node_dict = {}
    for node in nodes:  
        node_dict.setdefault(node[0], []).append(node[1])

    return node_dict

def generate_Graph(ptAr, tris):
    node_dict = generate_nodeDict(tris)
    aGraph = Graph(node_dict, ptAr)
    return aGraph


def euclidean_distance(pt1, pt2):
    x_diff = pt2[0] - pt1[0]
    y_diff = pt2[1] - pt1[1]
    z_diff = pt2[2] - pt1[2]
    return math.sqrt(x_diff*x_diff + y_diff*y_diff + z_diff*z_diff)

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

#@dask.delayed
def dijkstra_start_end(aGraph, start_vertex, end_vertex, reveal_path = False):
    start_t = time.time()
    print "Starting Dijkstra from vertex: " + str(start_vertex) + " to " + str(end_vertex)

    # aGraph = Graph(node_dict, ptAr)

    # Set the distance for the start node to zero 
    start = aGraph.get_vertex(start_vertex)

    end = aGraph.get_vertex(end_vertex)

    start.set_distance(0)

    # Put tuple pair into the priority queue
    print "Calculating unvisited_queue..."
    unvisited_queue = [(v.get_distance(),v) for v in aGraph]

    total_univisited_num = len(unvisited_queue)
    print "unvisited_queue calculated. "
#     print "unvisited queue: "
#     #print [t[1] for t in unvisited_queue]
#     for t in unvisited_queue:
#         print t[1]
#     print "End of the queue"
    heapq.heapify(unvisited_queue)

    print "Calculating the shortest path to each vertex..."

    pbar = tqdm(total = total_univisited_num)

    while len(unvisited_queue): # as long as there's an element in the list 
        # Pops a vertex with the smallest distance 
        uv = heapq.heappop(unvisited_queue)
        #print uv 
        current = uv[1]
        current.set_visited()

        # left_percent = (len(unvisited_queue)*1.0)/(total_univisited_num*1.0)
        # print str(left_percent) + " percent of total unvisited_queue is visited. "
        # pbar.set_description('processed: %d' % (1 + left_percent))

        if current == end:
            print "Reached the destination vertex! :D  "
            break

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
        pbar.update(1)

    pbar.close()

    path = [end.get_id()]

    shortest(end, path) # path is from the target to the source
    
    path_reverse = path[::-1] # this reverses the order. 


    print "Dijkstra is done. "
    graph_vert_dict = aGraph.get_vert_dict()
    
    # distance_matrix = []
    
    # for target_vertex in range(len(graph_vert_dict)):
    #     distance_matrix.append(graph_vert_dict[target_vertex].get_distance())
     
    end_t = time.time()

    print "This dijkstra process took: " + str(end_t-start_t) + " seconds"

    if reveal_path == True:
        return graph_vert_dict[end_vertex].get_distance(), path_reverse

    else:
        return graph_vert_dict[end_vertex].get_distance()




# #### MAIN PART ####

# from dask import delayed
# import dask
# from dask.diagnostics import ProgressBar
# import dask.multiprocessing
# import pickle

# start_t = time.time()

# def does_nothing(input):
#     return input 
    
# ### PARAMETERS
# start_index = 2000 ### THIS NEEDS TO BE CHANGED WHEN RUNNING ANOTHER DATASET
# end_index = 4*len(node_dict)/5
# core_use = 39

# file_Name_mid = "Tangential_MarchingAlg_convex-hulled_double_meshed_katz_mid.pkl"
# file_Name_final = "Tangential_MarchingAlg_convex-hulled_double_meshed_katz_final.pkl"

# ###

# index_range = range(start_index, end_index, core_use)

# last_start_index = index_range[-1]
# last_end_index = end_index
# dist_mat_joined = []

# print "PYTHON SCRIPT STARTS:"
# print "Start Index: " + str(start_index)
# print "End Index: " + str(end_index-1)

# for t in range(len(index_range)-1):
#     print "Running on the range from " + str(index_range[t]) + " to " + str(index_range[t+1]-1)
#     with dask.diagnostics.ProgressBar():
#         dist_mat_process = [delayed(dijkstra)(node_dict, ptAr, i) for i in range(index_range[t], index_range[t+1])]
#         dist_mat_cal = delayed(does_nothing)(dist_mat_process)
#         dist_mat = dist_mat_cal.compute(num_workers = core_use, get=dask.multiprocessing.get)
    
#     dist_mat_joined.append(dist_mat)
    
#     # open the file for writing
#     fileObject = open(file_Name_mid,'wb') 

#     pickle.dump(dist_mat_joined,fileObject)   
    
#     # here we close the fileObject
#     fileObject.close()
    
# end_t = time.time()


# print "running on the range from " + str(last_start_index)+ " to " + str(last_end_index)

# ## Remaining piece 

# dist_mat_process = [delayed(dijkstra)(node_dict, ptAr, i) for i in range(last_start_index, last_end_index)]
# dist_mat_cal = delayed(does_nothing)(dist_mat_process)
# dist_mat = dist_mat_cal.compute(get=dask.multiprocessing.get)
# dist_mat_joined.append(dist_mat)

# # open the file for writing
# fileObject = open(file_Name_final,'wb') 

# pickle.dump(dist_mat_joined,fileObject)   

# # here we close the fileObject
# fileObject.close()
# print "Dijkstra's algorithm is done running. "

# # # we open the file for reading
# # fileObject = open(file_Name,'r')  
# # # load the object from the file into var b
# # dist_mat_loaded = pickle.load(fileObject)  





