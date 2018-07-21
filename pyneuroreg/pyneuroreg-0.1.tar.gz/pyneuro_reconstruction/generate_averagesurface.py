from pyneuro_io import amiraparsing as ap
import pyneuro_reconstruction.icp as icp
import pyneuro_reconstruction.triangleresampler as trs

import numpy as np
import math


def generate_averageSurf_byfile(src_surf_file, tg_surf_file):

	# src_surf_file1 is a source surface file. The reference surface. 
	# tg_surf_fil1 is a target surface file. 

	src_sff = ap.amiraParsingSurface(src_surf_file)
	src_sf = ap.convertToNParray(src_sff[0])

	tg_sff = ap.amiraParsingSurface(tg_surf_file)
	tg_sf = ap.convertToNParray(tg_sff[0])

	print "Files are loaded. "

	src_tris_raw = ap.convertToInt(src_sff[1])
	src_tris = []
	for tri in src_tris_raw:
		new_tri = np.array(tri) - np.array([1,1,1])
		src_tris.append(tuple(new_tri))
		

	tg_tris_raw = ap.convertToInt(tg_sff[1])
	tg_tris = []
	for tri in tg_tris_raw:
		new_tri2 = np.array(tri) - np.array([1,1,1])
		tg_tris.append(tuple(new_tri2))

	print "starting resampling..."
	src_sf_rs = trs.resample_surface(src_sf, src_tris)
	tg_sf_rs = trs.resample_surface(tg_sf, tg_tris)

	print "done resampling"
	# choose which to downsample 

	if src_sf_rs.shape[0] > tg_sf_rs.shape[0]:
		sampled_indice = np.random.choice(src_sf_rs.shape[0], tg_sf_rs.shape[0], replace=False)
		src_rs_ds = src_sf_rs[sampled_indice]

		print "starting icp..."
		T, distances, i, nrb_indices = icp.icp(src_rs_ds, tg_sf_rs)
		tg_sf_nrb = tg_sf_rs[nrb_indices]

		print "icp done"
		sf_avg = (src_rs_ds + tg_sf_nrb)/2 




	if src_sf_rs.shape[0] < tg_sf_rs.shape[0]:
		sampled_indice = np.random.choice(tg_sf_rs.shape[0], src_sf_rs.shape[0], replace=False)
		tg_rs_ds = tg_sf_rs[sampled_indice]

		print "starting icp..."
		T, distances, i, nrb_indices = icp.icp(src_sf_rs, tg_rs_ds)
		tg_sf_nrb = tg_rs_ds[nrb_indices]

		print "icp done"
		sf_avg = (src_sf_rs + tg_sf_nrb)/2 



	return sf_avg
	# resort the target point cloud to match the indexing of the source cloud by nearest neighbors 



def generate_averageSurf(src_pt_cloud, tg_pt_cloud):

	src_sf_rs = src_pt_cloud
	tg_sf_rs = tg_pt_cloud

	if src_sf_rs.shape[0] > tg_sf_rs.shape[0]:
		sampled_indice = np.random.choice(src_sf_rs.shape[0], tg_sf_rs.shape[0], replace=False)
		src_rs_ds = src_sf_rs[sampled_indice]

		print "starting icp..."
		T, distances, i, nrb_indices = icp.icp(src_rs_ds, tg_sf_rs)
		tg_sf_nrb = tg_sf_rs[nrb_indices]

		src_rs_ds_tfd = icp.transform(src_rs_ds, T)

		print "icp done"
		sf_avg = (src_rs_ds_tfd + tg_sf_nrb)/2 


	if src_sf_rs.shape[0] < tg_sf_rs.shape[0]:
		sampled_indice = np.random.choice(tg_sf_rs.shape[0], src_sf_rs.shape[0], replace=False)
		tg_rs_ds = tg_sf_rs[sampled_indice]

		print "starting icp..."
		T, distances, i, nrb_indices = icp.icp(src_sf_rs, tg_rs_ds)
		tg_sf_nrb = tg_rs_ds[nrb_indices]

		src_sf_rs_tfd = icp.transform(src_sf_rs, T)

		print "icp done"
		sf_avg = (src_sf_rs_tfd + tg_sf_nrb)/2 

	return sf_avg
	# resort the target point cloud to match the indexing of the source cloud by nearest neighbors 


def generate_averageSurf_list(pt_cloud_list):
	# the first cloud serves as the reference. 

	avg_cloud = pt_cloud_list[0]

	for i in range(len(pt_cloud_list)-1):
		avg_cloud = generate_averageSurf(pt_cloud_list[i+1], avg_cloud)

	return avg_cloud


def register_to_Surf(src_pt_cloud, tg_pt_cloud):

	# register to the target surface
	# returns the registered source surface and the transfomration matrix 

	src_sf_rs = src_pt_cloud
	tg_sf_rs = tg_pt_cloud

	if src_sf_rs.shape[0] > tg_sf_rs.shape[0]:
		sampled_indice = np.random.choice(src_sf_rs.shape[0], tg_sf_rs.shape[0], replace=False)
		src_rs_ds = src_sf_rs[sampled_indice]

		print "starting icp..."
		T, distances, i, nrb_indices = icp.icp(src_rs_ds, tg_sf_rs)
		src_tfd = icp.transform(src_rs_ds, T)

		print "icp done"
		


	if src_sf_rs.shape[0] < tg_sf_rs.shape[0]:
		sampled_indice = np.random.choice(tg_sf_rs.shape[0], src_sf_rs.shape[0], replace=False)
		tg_rs_ds = tg_sf_rs[sampled_indice]

		print "starting icp..."
		T, distances, i, nrb_indices = icp.icp(src_sf_rs, tg_rs_ds)
		src_tfd = icp.transform(src_rs_ds, T)

		print "icp done"

	return src_tfd, T
	# resort the target point cloud to match the indexing of the source cloud by nearest neighbors 


def register_To_averageSurf_list(avg_cloud, pt_cloud_list):
	# the first cloud serves as the reference. 
	registered_list = []

	for i in range(len(pt_cloud_list)):
		registered = register_to_Surf(pt_cloud_list[i], avg_cloud)
		registered_surf = registered[0]
		registering_T = registered[1]

		registered_list.append(registered_surf, registering_T)

	return registered_list





