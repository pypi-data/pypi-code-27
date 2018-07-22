import numpy as np
from scipy.spatial import Delaunay

# Create a meshed surface from a point cloud
# Written by Peter Park 


def mesh_surface(pt_cloud):
	pt_cloud_delau = Delaunay(pt_cloud)


	# if amira_ready == True: # The indexing on amira starts from 1. 
	# 	tri_list = []

	# 	for tri in pt_cloud_delau.simplices:
	# 	    tri_list.append([tri[0]+1,tri[1]+1,tri[2]+1])
	# 	    tri_list.append([tri[1]+1,tri[2]+1,tri[3]+1])
	# 	    tri_list.append([tri[0]+1,tri[1]+1,tri[3]+1])
	# 	    tri_list.append([tri[2]+1,tri[0]+1,tri[3]+1])

	# 	tri_list_np = np.asarray(tri_list)


# else: # The default indexing by delaunay starts from 0. 
	tri_list = []

	for tri in pt_cloud_delau.simplices:
	    tri_list.append([tri[0],tri[1],tri[2]])
	    tri_list.append([tri[1],tri[2],tri[3]])
	    tri_list.append([tri[0],tri[1],tri[3]])
	    tri_list.append([tri[2],tri[0],tri[3]])

	tri_list_np = np.asarray(tri_list) + [1,1,1]


	return tri_list_np


def convexhull_surface(pt_cloud):
	pt_cloud_delau = Delaunay(pt_cloud)

	tris = pt_cloud_delau.convex_hull

	tris_np = np.asarray(tris) + [1,1,1]

	return tris_np
	