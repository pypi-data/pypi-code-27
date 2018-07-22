from pyneuro_io import amiraparsing as ap
import numpy as np
#import time
#%matplotlib notebook
from pyneuro_io import landmarkwriter as lw
from . import flatmaptransform as ft
import math
import pyneuro_io.surfacewriter as sw
import copy

version_num = 0.52 # March 20. 2018

print "flatmaprep Version: " + str(version_num)
'''
Creates an array of scale_factors for a 3D surface such that they minimize the distance
between the surface and each landmark

'''
### HELPER FUNCTION 
# Polar Coords: phi (on x-y plane), theta (on with z-axis), radius
def toPolar(ptAr):
	phi = np.arctan2(ptAr[:,1], ptAr[:,0])
	phi = phi.reshape((len(phi),1))
	
	r_xy = np.sqrt(np.square(ptAr[:,0])+ np.square(ptAr[:,1]))
	theta = np.arctan2(ptAr[:,2], r_xy)
	theta = theta.reshape((len(theta),1))
	
	r_z = np.sqrt(np.square(r_xy) + np.square(ptAr[:,2]))
	r_z = r_z.reshape((len(r_z),1))
	
	return np.hstack((r_z, phi, theta))


def toCartesian(ptAr):
	r_z = ptAr[:,0] 
	phi = ptAr[:,1]
	theta = ptAr[:,2]
	
	z = r_z * np.sin(theta)
	z = z.reshape((len(z), 1))
	
	r_xy = r_z * np.cos(theta)
	y = r_xy * np.sin(phi)
	y = y.reshape((len(y), 1))
	x = r_xy * np.cos(phi)
	x = x.reshape((len(x), 1))
	
	## Bottom-Centering
	ptAr_surface = np.hstack((x, y, z))
	n = len(ptAr_surface)
	j_mat = np.eye(n) - np.multiply(np.ones((n,n)), 1.0/n)
	ptAr_surface_C = np.matmul(j_mat, ptAr_surface)
	
	bottom = min(ptAr_surface_C[:,2])
	ptAr_surface_CB = ptAr_surface_C - [0, 0, bottom] 
	
	return ptAr_surface_CB
	  
# Shrinking with respect to the Bottom COM
def polarScale(ptAr_polar, scale_factor):
	ptAr_polar_copy = copy.deepcopy(ptAr_polar)
	ptAr_polar_copy[:,0] = ptAr_polar_copy[:,0] * scale_factor 
	return ptAr_polar_copy
	
### USE THIS FUNCTION TO SCALE 
def scale_surface(ptAr, scale_factor):
	ptAr_polar = toPolar(ptAr)
	ptAr_polar_scaled = polarScale(ptAr_polar, scale_factor)
	ptAr_result = toCartesian(ptAr_polar_scaled)
	return ptAr_result

def findClosestPoint(pt, ptAr):
	dist = np.sqrt(np.sum((ptAr - pt)**2, axis=1))
	return np.argmin(dist)

def findMinDist(pt, ptAr):
	dist = np.sqrt(np.sum((ptAr - pt)**2, axis=1))
	return np.min(dist)

## Assuming the surface and the landmarks are centered 
## Otherwise, run centerer.py

def calculateScale(ptAr_surface, ptAr_landmark):
	print "Calculating scaling for the landmark group... "
	print "# of landmarks: " + str(len(ptAr_landmark))
	# n == len(ptAr_landmark)
	scale_list = [] 
	scale_range = range(100, 4, -1) # Sweeping from 100% to 5%
	print "Sweep Range: from 100 to " + str(scale_range[-1])
	index_count  = 0
	for landmark_point in ptAr_landmark:
		print "Calculating scaling for Landmark Index: " + str(index_count)
		index_count = index_count + 1
		dist_set_1pt = []

		for scale_f in scale_range:
			scale_factor = scale_f *0.01
			#print scale_factor
			ptAr_surface_c_reduced = scale_surface(ptAr_surface, scale_factor)
			min_dist = findMinDist(landmark_point, ptAr_surface_c_reduced)
			dist_set_1pt.append(min_dist)

		argmin = np.argmin(dist_set_1pt)
		scale_f_point = scale_range[argmin]*0.01
		scale_list.append(scale_f_point)

	scale_list_np = np.array(scale_list)

	return scale_list_np

def calculateScale_one(ptAr_surface, landmark):
	# n == len(ptAr_landmark)
	scale_range = range(100, 4, -1) # Sweeping from 100% to 5% by 1 % step-size
	dist_set_1pt = []
	for scale_f in scale_range:
		scale_factor = scale_f *0.01
		#print scale_factor
		ptAr_surface_c_reduced = scale_surface(ptAr_surface, scale_factor)
		min_dist = findMinDist(landmark, ptAr_surface_c_reduced)
		dist_set_1pt.append(min_dist)

	argmin = np.argmin(dist_set_1pt)
	scale_f_point = scale_range[argmin]*0.01
	return scale_f_point



# calcaulte the scaledown for the landmark that corresponds to the mean of top 5 percernt
def calculateScaledown(ptAr_surface, landmark_flat_group, landmark_3D_group):
	bottom_num = len(landmark_flat_group[:,2])/15 # top 5 percent

	bottom = np.sort(landmark_flat_group[:,2])[0:bottom_num]
	bottom_index = np.argsort(landmark_flat_group[:,2])[0:bottom_num]

	mean_b = np.mean(bottom)
	b_argmin = np.argmin(abs(bottom - mean_b))

	bottom_landmark_index = bottom_index[b_argmin]
	BottomLayer_landmark = landmark_3D_group[bottom_landmark_index]

	scaledown = calculateScale_one(ptAr_surface, BottomLayer_landmark)

	return scaledown


# calcaulte the scaledown for the landmark that corresponds to the mean of top 5 percernt
def calculateScaledown_debug(ptAr_surface, landmark_flat_group, landmark_3D_group):
	bottom_num = len(landmark_flat_group[:,2])/20 # top 5 percent

	bottom = np.sort(landmark_flat_group[:,2])[0:bottom_num]
	bottom_index = np.argsort(landmark_flat_group[:,2])[0:bottom_num]

	mean_b = np.mean(bottom)
	b_argmin = np.argmin(abs(bottom - mean_b))

	bottom_landmark_index = bottom_index[b_argmin]
	BottomLayer_landmark = landmark_3D_group[bottom_landmark_index]

	scaledown = calculateScale_one(ptAr_surface, BottomLayer_landmark)

	return scaledown, BottomLayer_landmark, bottom_landmark_index


# the flatmap should be centered as well (I think?)
def flatmaprep(ptAr_flatmap, ptAr_surface, ptAr_landmark):
	print "Calculating scaling... "
	scale_list = calculateScale(ptAr_surface, ptAr_landmark)
	print "Scale list calculated"
	argmin_set = []
	min_dist_set = []
	for t in range(len(ptAr_landmark)):
		min_dist = findMinDist(ptAr_landmark[t], ptAr_surface)
		min_index = findClosestPoint(ptAr_landmark[t], ptAr_surface)
		min_dist_set.append(min_dist_set)
		argmin_set.append(min_index)

	ptAr_landmark_flat = ptAr_flatmap[argmin_set][:, 0:2]

	min_dist_set = np.asarray(min_dist_set)
	min_dist_set = min_set.reshape((len(min_dist_set),1))

	flat_scale_list = np.square(scale_list)

	ptAr_flatmap_reps= []
	for lm_index in range(0, len(ptAr_landmark)):
		ptAr_flatmap_rescaled = scale_surface(ptAr_flatmap, flat_scale_list[lm_index])
		ptAr_flatmap_reps.append(ptAr_flatmap_rescaled[lm_index])

	ptAr_flatmap_reps_np = np.asarray(ptAr_flatmap_reps)

	return ptAr_flatmap_reps_np

def getGeodesicAndEuclideanMat(scaling_factor, landmarks_3D, flatmap_ptAr, surface_ptAr, gd_mat):
    surface_ptAr_scaled = scale_surface(surface_ptAr, scaling_factor)
    gd_mat_scaled = scaling_factor * gd_mat
    gd_mat_flat_scaled = scaling_factor * gd_mat
    flatmap_ptAr_scaled = scale_surface(flatmap_ptAr, scaling_factor)
    
    target_area_index = ft.flatmaptransform_index2(landmarks_3D, flatmap_ptAr_scaled, surface_ptAr_scaled)
    target_dist_mat_N= len(target_area_index)
    
    landmark_flat_scaled = flatmap_ptAr_scaled[target_area_index]
    euclidean_mat_target_flat = np.zeros((target_dist_mat_N, target_dist_mat_N)) # Initialize

    for i in range(target_dist_mat_N):
        for k in range(target_dist_mat_N):
            if i == k:
                euclidean_mat_target_flat[i,k] = 0

            else:
                euclidean_mat_target_flat[i,k] = interdistance(landmark_flat_scaled[i], landmark_flat_scaled[k])

    geodesic_mat_target = np.zeros((target_dist_mat_N, target_dist_mat_N)) # Initialize
    
    for i in range(target_dist_mat_N):
        for k in range(target_dist_mat_N):
            if i == k:
                geodesic_mat_target[i,k] = 0

            else:
                x = target_area_index[i]
                y = target_area_index[k]
                geodesic_mat_target[i,k] = gd_mat_scaled[x, y] 

    return geodesic_mat_target, euclidean_mat_target_flat


def interdistance_xy(ptAr1, ptAr2):
    return math.sqrt(np.square(ptAr1[0]-ptAr2[0]) + np.square(ptAr1[1]-ptAr2[1]))


def interdistance(ptAr1, ptAr2):
    return math.sqrt(np.square(ptAr1[0]-ptAr2[0]) + np.square(ptAr1[1]-ptAr2[1]) + np.square(ptAr1[2]-ptAr2[2]))