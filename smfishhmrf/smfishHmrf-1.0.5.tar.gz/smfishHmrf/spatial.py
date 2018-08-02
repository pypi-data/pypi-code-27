import scipy
import scipy.stats
import sys
import re
import os
import numpy as np
import math
from scipy.spatial.distance import squareform, pdist
from scipy.stats import percentileofscore
import smfishHmrf.reader as reader

def read(n):
	f = open(n)
	h = f.readline().rstrip("\n").split(" ")[1:]
	num_g = len(h)
	num_c = 1
	for l in f:
		l = l.rstrip("\n")
		ll = l.split(" ")
		num_c+=1
	f.close()
	mat = np.empty((num_g, num_c), dtype="float32")

	f = open(n)
	c = 0
	for l in f:
		l = l.rstrip("\n")
		ll = l.split(" ")
		this_cell = ll[0]
		val = [float(v) for v in ll[1:]]
		mat[:,c] = val
		c+=1
	f.close()
	return mat

def get_distance_per_FD(mr_dissimilarity_FD, num_cell, clust):
	within_dist = {}
	across_dist = {}
	#m1 = np.where((field==100))[0]
	for i in range(num_cell):
		this_i = i
		within_dist.setdefault(this_i, [])
		across_dist.setdefault(this_i, {})
		for j in range(i+1, num_cell):
			this_j = j
			within_dist.setdefault(this_j, [])
			across_dist.setdefault(this_j, {})
			dist = mr_dissimilarity_FD[i, j]
			if clust[this_i]==clust[this_j]:
				within_dist[this_i].append(dist)
				within_dist[this_j].append(dist)
			else:
				across_dist[this_i].setdefault(clust[this_j], [])
				across_dist[this_j].setdefault(clust[this_i], [])
				across_dist[this_i][clust[this_j]].append(dist)
				across_dist[this_j][clust[this_i]].append(dist)
	silhouette = {}
	np_silhouette = np.zeros((num_cell), dtype="float32")
	#k = 10
	for pt in within_dist:
		if len(within_dist[pt])<5:
			continue
		mm = np.mean(within_dist[pt])
		across = []
		for cl2 in across_dist[pt]:
			if len(across_dist[pt][cl2])<5:
				continue
			#across_sort = np.sort(across_dist[pt][cl2])
			across.append(np.mean(across_dist[pt][cl2]))
			#across.append(np.mean(across_sort[:k]))
		if len(across)==0:
			continue
		mn = np.min(across)
		silhouette[pt] = float(mn - mm)/max(mn, mm)
		np_silhouette[pt] = silhouette[pt]
	avg_silhouette = 0
	for pt in silhouette:
		avg_silhouette+=silhouette[pt]
	avg_silhouette/=len(silhouette.keys())
	return avg_silhouette, np_silhouette	

def rank_transform_matrix(mat, rbp_p = 0.99, reverse=True):
	dim1 = mat.shape[0]
	dim2 = mat.shape[1]
	rank_forward = np.empty([dim1, dim2])
	for c1 in range(dim1):
		rd = scipy.stats.rankdata(mat[c1,:])
		if reverse==True:
			rd = dim2 - rd + 1
		rank_forward[c1, :] = rd
	rank_backward = np.empty([dim1, dim2])
	for c1 in range(dim2):
		rd = scipy.stats.rankdata(mat[:,c1])
		if reverse==True:
			rd = dim1 - rd + 1
		rank_backward[:, c1] = rd
	mutual_rank_rbp = np.empty([dim1, dim2])
	mutual_rank = np.empty([dim1, dim2])
	for c1 in range(dim1):
		for c2 in range(dim2):
			ma = math.sqrt(rank_forward[c1, c2] * rank_backward[c1, c2])
			mutual_rank_rbp[c1, c2] = (1-rbp_p) * math.pow(rbp_p, ma - 1) 
			mutual_rank[c1, c2] = ma
	dissimilarity = np.empty([dim1, dim2])
	for c1 in range(dim1):
		for c2 in range(dim2):
			dissimilarity[c1, c2] = 1 - mutual_rank_rbp[c1, c2] / (1-rbp_p)
	return dissimilarity

def calc_silhouette_per_gene(genes=None, expr=None, dissim=None, examine_top=0.1, permutation_test=True, permutations=100):
	if genes is None or expr is None or dissim is None:
		sys.stderr.write("Need genes, expr, dissim\n")
		return ;

	print "Started"
	sil = []
	ncell = expr.shape[1]

	ex = int((1.0-examine_top)*100.0)
	for ig,g in enumerate(genes):
		print g, ig, "/", len(genes)
		cutoff = np.percentile(expr[ig,:], ex)
		clust = np.zeros((ncell), dtype="int32")
		clust[np.where(expr[ig,:]>=cutoff)[0]] = 1
		clust[np.where(expr[ig,:]<cutoff)[0]] = 2
		avg_sil_rank, all_silhouette = get_distance_per_FD(dissim, ncell, clust)
		sil.append((g, avg_sil_rank, np.mean(all_silhouette[np.where(clust==1)[0]])))

	res = []
	if permutation_test:
		print "Permutation test..."
		rand_clust = np.zeros((ncell), dtype="int32")
		rand_clust[0:int(ncell*(1.0 - examine_top))] = 2
		rand_clust[int(ncell*(1.0 - examine_top)):] = 1
		rand_sil = []
		for i in range(permutations):
			if i%10==0:
				print "Done", i, "/", permutations
			np.random.shuffle(rand_clust)
			r_avg_sil_rank, r_all_silhouette = get_distance_per_FD(dissim, ncell, rand_clust)
			rand_sil.append((r_avg_sil_rank, np.mean(r_all_silhouette[np.where(rand_clust==1)[0]])))

		r_avg = np.array([a[0] for a in rand_sil])
		r_sil = np.array([a[1] for a in rand_sil])
		for ig,g in enumerate(genes):
			this_avg = sil[ig][1]
			this_sil = sil[ig][2]
			#print g, this_avg, this_sil, scipy.stats.percentileofscore(r_avg, this_avg), \
			#scipy.stats.percentileofscore(r_sil, this_sil)
			res.append((g, this_sil, (100.0 - percentileofscore(r_sil, this_sil))/100.0))
	else:
		for ig,g in enumerate(genes):
			res.append((g, this_sil))
	res.sort(lambda x,y:cmp(x[1], y[1]), reverse=True)
	return res


if __name__=="__main__":
	#cortex_FDs = [100]
	directory = "hmrfem.whole.brain.e.fd0-48.correlated.gene"
	roi = "cortex"
	#FDs = cortex_FDs
	workdir = "/home/qz64/hmrf.submit"
	genes = reader.read_genes("%s/%s/genes" % (workdir, directory))
	Xcen, field = reader.read_coord("%s/%s/pca_corrected_cortex/f%s.coordinates.txt" % (workdir, directory, roi)) #note the stitched version use the .2 version
	Xcen = Xcen[1:]
	field = field[1:]
	#mat = read("%s/%s/bias_corrected_cortex/f%s.expression.txt" % (workdir, directory, roi))
	mat = np.transpose(reader.read_expression_matrix("%s/%s/pca_corrected_cortex/f%s.expression.txt" % (workdir, directory, roi)))
	#print expr.shape

	print Xcen.shape
	ncell = Xcen.shape[0]
	print "Euclidean distance"
	euc = squareform(pdist(Xcen, metric="euclidean"))
	print "Rank transform"
	dissim = rank_transform_matrix(euc, reverse=False, rbp_p=0.95)
	
	res = calc_silhouette_per_gene(genes=genes, expr=mat, dissim=dissim, examine_top=0.1, permutation_test=True, permutations=100)
	for i,j,k in res:
		print i,j,k
