from pyneuro_io import amiraparsing as ap
import numpy as np
from pyneuro_io import landmarkwriter as lw
import math
from pyneuro_io import surfacewriter as sw
import copy

'''
Centers a 3D surface: flips it (in x,y,z) and brings the bottom center of mass to the origin point
transforms a landmark group by the offset between the original surface and the centered surface

'''
Version = 0.59 # March 26. 2018

# Specific for tangential
def makecenter_file(surface_file, output_file):
	sf1 = ap.amiraParsingSurface2(surface_file)
	ptAr_surface_raw = np.asarray(ap.convertToFloat(sf1[0]))

	ptAr_surface = copy.deepcopy(ptAr_surface_raw)
	ptAr_surface[:,0] = ptAr_surface[:,0]
	ptAr_surface[:,1] = -ptAr_surface[:,1]
	ptAr_surface[:,2] = -ptAr_surface[:,2]


	n = len(ptAr_surface)
	j_mat = np.eye(n) - np.multiply(np.ones((n,n)), 1.0/n)
	ptAr_surface_C = np.matmul(j_mat, ptAr_surface)

	bottom = min(ptAr_surface_C[:,2])
	ptAr_surface_CB = ptAr_surface_C - [0, 0, bottom] 

	sw.writeSurface(surface_file, output_file, ptAr_surface_CB)

# When centering, we need to switch the x-axis, y-axis, z-axis to match
def changeAxis_tangential(surface_ptAr_raw):
	ptAr_surface = copy.deepcopy(surface_ptAr_raw)
	ptAr_surface_new = copy.deepcopy(ptAr_surface)

	ptAr_surface_new[:, 0] = ptAr_surface[:,0]
	ptAr_surface_new[:, 1] = -ptAr_surface[:,1]
	ptAr_surface_new[:, 2] = -ptAr_surface[:,2]

	return ptAr_surface_new

# When centering, we need to switch the x-axis, y-axis, z-axis to match the tangential
def changeAxis_coronal_left(surface_ptAr_raw):
	ptAr_surface = copy.deepcopy(surface_ptAr_raw)
	ptAr_surface_new = copy.deepcopy(ptAr_surface)

	ptAr_surface_new[:, 0] = -ptAr_surface[:, 1]
	ptAr_surface_new[:, 1] = -ptAr_surface[:, 2]
	ptAr_surface_new[:, 2] =  ptAr_surface[:, 0]

	return ptAr_surface_new

# When centering, we need to switch the x-axis, y-axis, z-axis to match the tangential
def changeAxis_coronal_right(surface_ptAr_raw):
	ptAr_surface = copy.deepcopy(surface_ptAr_raw)
	ptAr_surface_new = copy.deepcopy(ptAr_surface)

	ptAr_surface_new[:, 0] = ptAr_surface[:, 1]
	ptAr_surface_new[:, 1] = -ptAr_surface[:,2]
	ptAr_surface_new[:, 2] = -ptAr_surface[:,0]

	return ptAr_surface_new

########
# ## For flatmap-repair (if you hadn't centered the surface before creating a flatmap)
# def fixAxis_tangential(surface_ptAr_raw):
# 	ptAr_surface = copy.deepcopy(surface_ptAr_raw)
# 	ptAr_surface_new = copy.deepcopy(ptAr_surface)

# 	ptAr_surface_new[:, 0] = ptAr_surface[:,1]
# 	ptAr_surface_new[:, 1] = -ptAr_surface[:,0]
# 	ptAr_surface_new[:, 2] = ptAr_surface[:,2]

# 	return ptAr_surface_new

# def fixAxis_coronal_left(surface_ptAr_raw):
# 	ptAr_surface = copy.deepcopy(surface_ptAr_raw)
# 	ptAr_surface_new = copy.deepcopy(ptAr_surface)

# 	ptAr_surface_new[:, 0] = -ptAr_surface[:, 1]
# 	ptAr_surface_new[:, 1] = ptAr_surface[:, 0]
# 	ptAr_surface_new[:, 2] = ptAr_surface[:,2]

# 	return ptAr_surface_new

# def fixAxis_coronal_right(surface_ptAr_raw):
# 	ptAr_surface = copy.deepcopy(surface_ptAr_raw)
# 	ptAr_surface_new = copy.deepcopy(ptAr_surface)

# 	ptAr_surface_new[:, 0] = -ptAr_surface[:, 1] # to match the left 
# 	ptAr_surface_new[:, 1] = ptAr_surface[:, 0]
# 	ptAr_surface_new[:, 2] = ptAr_surface[:, 2]

# 	return ptAr_surface_new

def flip_X_axis(surface_ptAr_raw):
	ptAr_surface = copy.deepcopy(surface_ptAr_raw)
	ptAr_surface_new = copy.deepcopy(ptAr_surface)

	ptAr_surface_new[:, 0] = -ptAr_surface[:, 0] # to match the left 
	ptAr_surface_new[:, 1] = ptAr_surface[:, 1]
	ptAr_surface_new[:, 2] = ptAr_surface[:, 2]

	return ptAr_surface_new
#########
# Only for tangential 
def makecenter_ptAr_tangential(surface_ptAr_raw):
	ptAr_surface = changeAxis_tangential(copy.deepcopy(surface_ptAr_raw))

	n = len(ptAr_surface)
	j_mat = np.eye(n) - np.multiply(np.ones((n,n)), 1.0/n)
	ptAr_surface_C = np.matmul(j_mat, ptAr_surface)

	bottom = min(ptAr_surface_C[:,2])
	ptAr_surface_CB = ptAr_surface_C - [0, 0, bottom] 

	return ptAr_surface_CB


def makecenter_ptAr_coronal(surface_ptAr_raw):
	ptAr_surface = changeAxis_coronal_left(copy.deepcopy(surface_ptAr_raw))

	n = len(ptAr_surface)

	j_mat = np.eye(n) - np.multiply(np.ones((n,n)), 1.0/n)

	ptAr_surface_C = np.dot(j_mat, ptAr_surface)
	bottom = min(ptAr_surface_C[:,2])
	ptAr_surface_CB = ptAr_surface_C - [0, 0, bottom] 

	return ptAr_surface_CB

def makecenter_ptAr_coronal_right(surface_ptAr_raw):
	ptAr_surface = changeAxis_coronal_right(copy.deepcopy(surface_ptAr_raw))

	n = len(ptAr_surface)

	j_mat = np.eye(n) - np.multiply(np.ones((n,n)), 1.0/n)

	ptAr_surface_C = np.dot(j_mat, ptAr_surface)
	bottom = min(ptAr_surface_C[:,2])
	ptAr_surface_CB = ptAr_surface_C - [0, 0, bottom] 

	return ptAr_surface_CB


def makecenter_ptAr_flatmap(surface_ptAr_raw):
	ptAr_surface = copy.deepcopy(surface_ptAr_raw)

	n = len(ptAr_surface)
	j_mat = np.eye(n) - np.multiply(np.ones((n,n)), 1.0/n)

	ptAr_surface_C = np.matmul(j_mat, ptAr_surface)

	return ptAr_surface_C


# For tangential model 
# To be revised to work with one landmark as well
def applyOffsetTransform_tangential(ptAr_raw, ptAr_new, landmark):  
    ptAr_raw_copy = changeAxis_tangential(copy.deepcopy(ptAr_raw))
    
    offset = ptAr_new - ptAr_raw_copy
    offset = offset[0,:]
    
    landmark_copy = changeAxis_tangential(copy.deepcopy(landmark))
    
    result = landmark_copy + offset 
    
    return result

# For coronal model 
def applyOffsetTransform_coronal_left(ptAr_raw, ptAr_new, landmark):  
    ptAr_raw_copy = changeAxis_coronal_left(copy.deepcopy(ptAr_raw))
    offset = ptAr_new - ptAr_raw_copy
    offset = offset[0,:]

    landmark_copy = changeAxis_coronal_left(copy.deepcopy(landmark))
    result = landmark_copy + offset 
    
    return result

# For coronal model 
def applyOffsetTransform_coronal_right(ptAr_raw, ptAr_new, landmark):  
    ptAr_raw_copy = changeAxis_coronal_right(copy.deepcopy(ptAr_raw))
    offset = ptAr_new - ptAr_raw_copy
    offset = offset[0,:]

    landmark_copy = changeAxis_coronal_right(copy.deepcopy(landmark))
    result = landmark_copy + offset 
    
    return result




