'''
Resamples 43 points per each triangle 

For resampling for triangulated surface 

Written by Peter Park 

'''
from pyneuro_io import amiraparsing as ap
import numpy as np
import itertools as itt
from numpy import linalg as LA


def centeroid(p0,p1,p2):
    # format: p_n = np.array([x, y, z])
    arr = np.vstack((p0, p1, p2))
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    sum_z = np.sum(arr[:, 2])
    center = np.array([sum_x/length, sum_y/length, sum_z/length])
    return center

def iter_unpack(input_list):
    unpacked = list(itt.chain(*input_list))
    while type(unpacked[0]) != np.ndarray:
        unpacked = list(itt.chain(*unpacked))
    return unpacked

def iter_unpack2(input_list):
    unpacked = list(itt.chain(*input_list))
    while len(unpacked[0]) != 4:
        unpacked = list(itt.chain(*unpacked))
    return unpacked

def unpack(input_list):
    return list(itt.chain(*input_list))

def calculate_area(triangle):
    p0 = triangle[0]
    p1 = triangle[1]
    p2 = triangle[2]

    v1 = p1 - p0
    v2 = p2 - p0

    area = 1/2.0 * LA.norm(np.cross(v1, v2))
    return area


def divide_triangle(triangle, collection):
    # given points: [(p0, p1, p2), centeroid]
    p0 = triangle[0]
    p1 = triangle[1]
    p2 = triangle[2]
    p3 = triangle[3]    
    
    # now calculate the new three points
    p4 = centeroid(p0, p2, p3)
    p5 = centeroid(p0, p1, p3)
    p6 = centeroid(p1, p2, p3)
    
    # three new triangles 
    new_triangle1_with_center = [p0, p2, p3, p4]
    new_triangle2_with_center = [p0, p1, p3, p5]
    new_triangle3_with_center = [p1, p2, p3, p6]
    
    new_triangle_list = [(new_triangle1_with_center), (new_triangle2_with_center), (new_triangle3_with_center)]
    
    collection.append(new_triangle_list)
    return new_triangle_list

def divide_triangle_list(triangle_list, collection):
    new_list = []
    for i in range(len(triangle_list)):
        new_list.append(divide_triangle(triangle_list[i], collection))
        
    new_list = iter_unpack2(new_list) 
    return new_list

def resample_tri(p0, p1, p2, tri_threshold):
    # tri_threshold is the maximum allowed surface area of a triangle for resampling

    p3 = centeroid(p0,p1,p2)
    start = [p0, p1, p2, p3]
    collection = []

    # tri_size = calculate_area([p0,p1,p2])
    # print "area of the original triangle: " + str(tri_size)

    result_list = divide_triangle(start, collection)
    triangle_list = divide_triangle_list(result_list, collection)
        
    while calculate_area(triangle_list[0][:-1]) > tri_threshold:
        triangle_list = divide_triangle_list(triangle_list, collection)
        # print "updated area of the smaller triangle: " +  str(calculate_area(triangle_list[0][:-1]))
    # triangle_list2 = divide_triangle_list(triangle_list, collection) # 43 points resampled per triangle 
    # triangle_list3 = divide_triangle_list(triangle_list2, collection) # 124 points resampled per triangle 
    # triangle_list4 = divide_triangle_list(triangle_list3, collection)
    # triangle_list5 = divide_triangle_list(triangle_list4, collection) # 1096 points resampled per triangle
    # triangle_list6 = divide_triangle_list(triangle_list5, collection) # 3283 points resampled per triangle 
    
    # print "updated area of the smaller triangle: " +  str(calculate_area(triangle_list[0][:-1]))
    collected = np.array(iter_unpack(collection))
    unique_collected,index = np.unique(collected, axis=0, return_index=True) # Note that indexing changes to the list being ordered by first element
    
    return collected[np.sort(index)] # reverses the indexing back to the original order

def resample_surface(ptAr_surf, tris, tri_threshold = 30000):
    ptAr_tris_list = [] # points per each triangle, follows the indexing of tris 
    i = 1

    for tri in tris:
        ind1 = tri[0]
        ind2 = tri[1]
        ind3 = tri[2]
        # print "Working on #" + str(i) + " triangle"
        new_ptAr = resample_tri(ptAr_surf[ind1], ptAr_surf[ind2], ptAr_surf[ind3], tri_threshold)
        ptAr_tris_list.append(new_ptAr)
        
        i = i + 1

    ptAr_tris_unpacked = iter_unpack(ptAr_tris_list)

    ptAr_tris = np.array(ptAr_tris_unpacked)

    return ptAr_tris

def resample_tri_tracked(p0, p1, p2, tri_threshold):
    # tri_threshold is the maximum allowed surface area of a triangle for resampling

    p3 = centeroid(p0,p1,p2)
    start = [p0, p1, p2, p3]
    collection = []

    # tri_size = calculate_area([p0,p1,p2])
    # print "area of the original triangle: " + str(tri_size)

    result_list = divide_triangle(start, collection)
    triangle_list = divide_triangle_list(result_list, collection)
    
    iteration_num = 0 

    while calculate_area(triangle_list[0][:-1]) > tri_threshold:
        triangle_list = divide_triangle_list(triangle_list, collection)
        iteration_num = iteration_num + 1
    
    # print "updated area of the smaller triangle: " +  str(calculate_area(triangle_list[0][:-1]))
    collected = np.array(iter_unpack(collection))
    unique_collected,index = np.unique(collected, axis=0, return_index=True) # Note that indexing changes to the list being ordered by first element
    
    return collected[np.sort(index)], iteration_num # reverses the indexing back to the original order

def resample_surface_tracked(ptAr_surf, tris, tri_threshold = 30000):
    ptAr_tris_list = [] # points per each triangle, follows the indexing of tris 
    i = 1

    iteration_list = []

    for tri in tris:
        ind1 = tri[0]
        ind2 = tri[1]
        ind3 = tri[2]
        # print "Working on #" + str(i) + " triangle"
        new_ptAr, iteration_num = resample_tri_tracked(ptAr_surf[ind1], ptAr_surf[ind2], ptAr_surf[ind3], tri_threshold)
        ptAr_tris_list.append(new_ptAr)
        iteration_list.append(iteration_num)
        
        i = i + 1

    ptAr_tris_unpacked = iter_unpack(ptAr_tris_list)

    ptAr_tris = np.array(ptAr_tris_unpacked)

    return ptAr_tris, iteration_list

def resample_tri_manual_iter(p0, p1, p2, iteration_num):
    # tri_threshold is the maximum allowed surface area of a triangle for resampling

    p3 = centeroid(p0,p1,p2)
    start = [p0, p1, p2, p3]
    collection = []

    # tri_size = calculate_area([p0,p1,p2])
    # print "area of the original triangle: " + str(tri_size)

    result_list = divide_triangle(start, collection)
    triangle_list = divide_triangle_list(result_list, collection)
    
    iteration_index = 0 

    while iteration_index < iteration_num:
        triangle_list = divide_triangle_list(triangle_list, collection)
        iteration_index = iteration_index + 1

    
    collected = np.array(iter_unpack(collection))
    unique_collected,index = np.unique(collected, axis=0, return_index=True) # Note that indexing changes to the list being ordered by first element
    
    return collected[np.sort(index)] # reverses the indexing back to the original order

def resample_surface_with_iter_list(ptAr_surf, tris, iteration_list):
    ptAr_tris_list = [] # points per each triangle, follows the indexing of tris 

    i = 0 
    for tri in tris:
        ind1 = tri[0]
        ind2 = tri[1]
        ind3 = tri[2]

        new_ptAr = resample_tri_manual_iter(ptAr_surf[ind1], ptAr_surf[ind2], ptAr_surf[ind3], iteration_list[i])

        i = i + 1
        ptAr_tris_list.append(new_ptAr)
        

    ptAr_tris_unpacked = iter_unpack(ptAr_tris_list)

    ptAr_tris = np.array(ptAr_tris_unpacked)

    return ptAr_tris    
