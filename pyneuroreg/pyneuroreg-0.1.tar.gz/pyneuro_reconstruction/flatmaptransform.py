from pyneuro_io import amiraparsing as ap
import numpy as np
import time 
import math
import pickle
from pyneuro_io import landmarkwriter as lw

## Written by Peter Park 

version_num = 0.51 # March 16. 2018

def findClosestPoint(pt, ptAr):
	dist = np.sqrt(np.sum((ptAr - pt)**2, axis=1))
	return np.argmin(dist)

def findMinDist(pt, ptAr):
	dist = np.sqrt(np.sum((ptAr - pt)**2, axis=1))
	return np.min(dist)

def findMinDist_Closest_Pt(pt, ptAr):
	dist = np.sqrt(np.sum((ptAr - pt)**2, axis=1))
	return np.min(dist), np.argmin(dist)

def flatmaptransform_file(landmark_file, flatmap_file, surface_file, output1, output2):

	landmark_input = landmark_file
	surface_input = surface_file
	flatmap_input = flatmap_file

	### Reading in files
	lndm = ap.amiraParsingLandmarks(landmark_input)
	ptAr_landmark = np.asarray(ap.convertToFloat(lndm))

	sf = ap.amiraParsingSurface(surface_input)
	ptAr_surface = np.asarray(ap.convertToFloat(sf[0]))

	sf2 = ap.amiraParsingSurface(flatmap_input)
	ptAr_flat = np.asarray(ap.convertToFloat(sf2[0]))

	argmin_set = []
	min_set = []
	for t in range(len(ptAr_landmark)):
		#print ptAr_landmark[t]
		min_dist = findMinDist(ptAr_landmark[t], ptAr_surface)
		min_index = findClosestPoint(ptAr_landmark[t], ptAr_surface)
		# print "min_dist: " + str(min_dist)
		# print "min_index: " + str(min_index)
		min_set.append(min_dist)
		argmin_set.append(min_index)

	min_set = np.asarray(min_set)
	min_set = min_set.reshape((len(min_set),1))

	## Z-depth = distance from the surface
	flat_projection = ptAr_flat[argmin_set][:,0:2]
	flat_projection = np.hstack((flat_projection, min_set))

	flat_onSurface = ptAr_flat[argmin_set]

	lw.writeLandmarkAscii(output1, flat_onSurface)
	lw.writeLandmarkAscii(output2, flat_projection)

	return flat_projection

def flatmaptransform(ptAr_landmark, ptAr_flat, ptAr_surface):

	argmin_set = []
	min_set = []
	for t in range(len(ptAr_landmark)):
		#print ptAr_landmark[t]
		min_dist = findMinDist(ptAr_landmark[t], ptAr_surface)
		min_index = findClosestPoint(ptAr_landmark[t], ptAr_surface)
		# print "min_dist: " + str(min_dist)
		# print "min_index: " + str(min_index)
		min_set.append(min_dist)
		argmin_set.append(min_index)

	min_set = np.asarray(min_set)
	min_set = min_set.reshape((len(min_set),1))

	## Z-depth = distance from the surface
	flat_projection = ptAr_flat[argmin_set][:,0:2]
	flat_projection = np.hstack((flat_projection, min_set))

	flat_onSurface = ptAr_flat[argmin_set]

	return flat_projection


def flatmaptransform_onsurface(ptAr_landmark, ptAr_flat, ptAr_surface):

	argmin_set = []
	min_set = []
	for t in range(len(ptAr_landmark)):
		#print ptAr_landmark[t]
		min_dist = findMinDist(ptAr_landmark[t], ptAr_surface)
		min_index = findClosestPoint(ptAr_landmark[t], ptAr_surface)
		# print "min_dist: " + str(min_dist)
		# print "min_index: " + str(min_index)
		min_set.append(min_dist)
		argmin_set.append(min_index)


	### Normalization for z-depth
	min_set = np.asarray(min_set)
	min_set = min_set.reshape((len(min_set),1))

	flat_onSurface = ptAr_flat[argmin_set]

	return flat_onSurface

# Finds the localized area on the 3D surface when calculating the flamap representations.
def localizeOn3DSurface(ptAr_landmark, ptAr_flat, ptAr_surface): 

	argmin_set = []
	min_set = []
	for t in range(len(ptAr_landmark)):
		#print ptAr_landmark[t]
		min_dist = findMinDist(ptAr_landmark[t], ptAr_surface)
		min_index = findClosestPoint(ptAr_landmark[t], ptAr_surface)
		# print "min_dist: " + str(min_dist)
		# print "min_index: " + str(min_index)
		min_set.append(min_dist)
		argmin_set.append(min_index)

	surface_projection = ptAr_surface[argmin_set]

	return surface_projection

# Finds the localized area on the 3D surface and flatmap when calculating the flamap representations.
def localizeOnBoth(ptAr_landmark, ptAr_flat, ptAr_surface): 

	argmin_set = []
	min_set = []
	for t in range(len(ptAr_landmark)):
		#print ptAr_landmark[t]
		min_dist = findMinDist(ptAr_landmark[t], ptAr_surface)
		min_index = findClosestPoint(ptAr_landmark[t], ptAr_surface)
		# print "min_dist: " + str(min_dist)
		# print "min_index: " + str(min_index)
		min_set.append(min_dist)
		argmin_set.append(min_index)

	surface_projection = ptAr_surface[argmin_set]

	flat_projection = ptAr_flat[argmin_set][:,0:2]
	flat_projection = np.hstack((flat_projection, min_set))
	flat_onSurface = ptAr_flat[argmin_set]

	return surface_projection, flat_onSurface

def flatmaptransform_index(landmark_file, flatmap_file, surface_file, output1, output2):

	landmark_input = landmark_file
	surface_input = surface_file
	flatmap_input = flatmap_file

	### Reading in files
	lndm = ap.amiraParsingLandmarks(landmark_input)
	ptAr_landmark = np.asarray(ap.convertToFloat(lndm))

	sf = ap.amiraParsingSurface2(surface_input)
	ptAr_surface = np.asarray(ap.convertToFloat(sf[0]))

	sf2 = ap.amiraParsingSurface2(flatmap_input)
	ptAr_flat = np.asarray(ap.convertToFloat(sf2[0]))

	argmin_set = []
	min_set = []
	for t in range(len(ptAr_landmark)):
		#print ptAr_landmark[t]
		min_dist = findMinDist(ptAr_landmark[t], ptAr_surface)
		min_index = findClosestPoint(ptAr_landmark[t], ptAr_surface)
		# print "min_dist: " + str(min_dist)
		# print "min_index: " + str(min_index)
		min_set.append(min_dist)
		argmin_set.append(min_index)

	min_set = np.asarray(min_set)
	min_set = min_set.reshape((len(min_set),1))

	## Z-depth = distance from the surface
	flat_projection = ptAr_flat[argmin_set][:,0:2]
	flat_projection = np.hstack((flat_projection, min_set))

	flat_onSurface = ptAr_flat[argmin_set]

	# lw.writeLandmarkAscii(output1, flat_onSurface)
	# lw.writeLandmarkAscii(output2, flat_projection)

	return argmin_set

def flatmaptransform_index2(ptAr_landmark, ptAr_flat, ptAr_surface):

	argmin_set = []
	min_set = []
	for t in range(len(ptAr_landmark)):
		#print ptAr_landmark[t]
		min_dist = findMinDist(ptAr_landmark[t], ptAr_surface)
		min_index = findClosestPoint(ptAr_landmark[t], ptAr_surface)
		# print "min_dist: " + str(min_dist)
		# print "min_index: " + str(min_index)
		min_set.append(min_dist)
		argmin_set.append(min_index)


	min_set = np.asarray(min_set)
	min_set = min_set.reshape((len(min_set),1))

	## Z-depth = distance from the surface
	flat_projection = ptAr_flat[argmin_set][:,0:2]
	flat_projection = np.hstack((flat_projection, min_set))

	flat_onSurface = ptAr_flat[argmin_set]

	# lw.writeLandmarkAscii(output1, flat_onSurface)
	# lw.writeLandmarkAscii(output2, flat_projection)

	return argmin_set

################# DEBUG
# directory = '/Users/peterpark/Library/Mobile Documents/com~apple~CloudDocs/Work/Image_processing_scripts/Tangential/TangentialData/'
# landmark_file = 'LandmarksWithin_output_dec14_simplified.landmarkAscii'
# flatmap_file = 'output_dec14_2.am_mc_vtk_simplified_flat_rescaled.surf'
# surface_file = 'output_dec14_2.am_mc_vtk_simplified.surf' # rough surface

# flatmaptransform(directory+landmark_file, directory+flatmap_file, directory+surface_file)
# print "DONE"

# print "flatmaptransform Version: " + str(version_num)
########################



