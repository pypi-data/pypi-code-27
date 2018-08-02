import numpy as np
import math
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import smfishHmrf.reader as reader
import scipy
import scipy.stats
from sklearn.decomposition import PCA
from sklearn.utils.extmath import randomized_svd
from sklearn.manifold import TSNE
#sys.path.insert(0, "/home/qz64/hmrf.submit")
import os
#import rank_transform
#import calculate_overlap
sys.setrecursionlimit(10000)

#gene by gene correction
#requires expr, Xcen, field, FDs, num_bin
def calc_bias_moving(expr=None, centroid=None, field=None, interest_field=None, num_bin=10):
	if expr is None or centroid is None or field is None or interest_field is None:
		sys.stderr.write("Need expr, centroid, field, interest_field\n")
		return ;
	Xcen = centroid
	FDs = interest_field
	good_i = []
	for i in range(Xcen.shape[0]):
		if field[i] in set(FDs):
			good_i.append(i)
	good_i = np.array(good_i)
	expr = expr[good_i]
	Xcen = Xcen[good_i]
	field = field[good_i]
	#field specific average
	average = {}
	isCenter = np.empty(Xcen.shape[0], dtype="int32")
	for i in range(Xcen.shape[0]):
		if abs(Xcen[i,0])<1.0 and abs(Xcen[i,1])<1.0:
			isCenter[i] = 1
		else:
			isCenter[i] = 0
	for fd in sorted(FDs):
		m = np.where((field==fd) & (isCenter==1))[0]
		if np.isnan(np.mean(expr[m])):
			#if roi=="whole.brain.1e" and fd==39:
			#	average[fd] = average[38]
			print "Warning no cells in the center for field", fd, average[38]
		else:
			average[fd] = np.mean(expr[m])

	bin_size = 4.0 / num_bin
	cls = {}
	Xcen2 = Xcen
	bins = np.empty((num_bin, num_bin), dtype="float32")
	ct = np.empty((num_bin, num_bin), dtype="int32")
	val = {}
	for x in range(num_bin):
		for y in range(num_bin):
			bins[x,y] = 0
			ct[x,y] = 0
			val.setdefault((x,y), [])
	for i in range(Xcen2.shape[0]):
		t1 = int((max(min(Xcen2[i,0], 1.99), -1.99) - (-2.0)) / bin_size) 
		t2 = int((max(min(Xcen2[i,1], 1.99), -1.99) - (-2.0)) / bin_size) 
		val[(t1,t2)].append((expr[i], average[field[i]]))
		#print goi, t1, t2, expr[i], average[field[i]]
	moving_bins = [-2, -1, 0]
	#moving_bins = [-2, -1, 0, 1, 2]
	for x in range(num_bin):
		for y in range(num_bin):
			all_val = []
			for a in moving_bins:
				for b in moving_bins:
					if x+a>=0 and y+b>=0 and x+a<num_bin and y+b<num_bin: 
						all_val = all_val + val[(x+a, y+b)]
			all_expr = [t[0] for t in all_val]
			all_fd = [t[1] for t in all_val]
			bins[x,y] = np.sum(np.array(all_expr)) - np.sum(np.array(all_fd))
			#print goi, x,y,bins[x,y]
			ct[x,y] = len(all_expr)
			if ct[x,y]==0:
				bins[x,y] = 0
			else:
				bins[x,y] = bins[x,y] / float(ct[x,y])
	bins3 = np.empty((num_bin, num_bin), dtype="float32")
	for x in range(num_bin):
		for y in range(num_bin):
			bins3[x,y] = 0
	#xn = np.empty((num_bin, num_bin), dtype=np.uint8)
	for x in range(num_bin):
		for y in range(num_bin):
			if bins[y,num_bin-x-1]==0:
				#xn[x,y] = 127
				bins3[x,y] = 0
			else:
				#xn[x,y] = max(0, min(int((bins[y,num_bin-x-1] + 5.0) * 25.5),255))
				bins3[x,y] = bins[y,num_bin-x-1]
				#if xn[x,y] == 127:
				#	xn[x,y] = 128
				#	bins3[x,y] = 0
	#np.ndarray.flatten(xn).tofile("/tmp/example.%s.raw" % "tmp")
	#print np.max(bins3), np.min(bins3)
	return bins3

#bias is like the field bias map (across field averages)
def do_pca(expr=None, expr_bias=None, centroid=None, field=None, interest_field=None, num_bin=50, top_comp_remove=5):
	if expr is None or expr_bias is None or centroid is None or field is None or interest_field is None:
		sys.stderr.write("Need expr, expr_bias, centroid, field, interest_field\n")
		return ;
	Xcen = centroid
	FDs = interest_field
	ngene = expr.shape[0]
	U,Sigma,VT = randomized_svd(np.transpose(expr_bias), n_components=ngene, n_iter=20, random_state=None)
	print Sigma
	#print U.shape #2500, 125
	#print VT.shape #125, 125
	for i in range(top_comp_remove, Sigma.shape[0]):
		Sigma[i] = 0
	U_Sigma = np.matmul(U, np.diag(Sigma))
	transformed = np.matmul(U_Sigma, VT)
	expr_bias = np.transpose(transformed)

	bin_size = 4.0 / num_bin
	for ind in range(expr.shape[0]):
		bias = np.reshape(expr_bias[ind,], (num_bin, num_bin)) #reshaped bins
		for i in range(Xcen.shape[0]):
			if not field[i] in set(FDs):
				continue
			t1 = int((max(min(Xcen[i,0], 1.99), -1.99) - (-2.0)) / bin_size) 
			t2 = int((max(min(Xcen[i,1], 1.99), -1.99) - (-2.0)) / bin_size) 		
			x1 = num_bin-t2-1
			y1 = t1
			expr[ind,i] = expr[ind,i] - bias[x1,y1]
	return expr

def get_pivot2(n):
	df = {}
	nd1 = n.shape[0]
	nd2 = n.shape[1]
	for i in range(1, nd1+1):
		for j in range(1, nd2+1):
			df.setdefault(i, {})
			df[i][j] = n[i-1,j-1]
	df2 = pd.DataFrame(df)
	return df2

def plot_pca(expr_bias=None, num_bin=None, top_pc=None, out_file=None):
	if expr_bias is None or num_bin is None or top_pc is None or out_file is None:
		sys.stderr.write("Need expr_bias, num_bin, top_pc, out_file\n")
		return ;
	ngene = expr.shape[0]
	U,Sigma,VT = randomized_svd(np.transpose(expr_bias), n_components=ngene, n_iter=20, random_state=None)
	nrow = int(top_pc / 4)
	ncol = 4
	if top_pc%4!=0:
		nrow+=1
	unit_x = 3.5
	unit_y = 3
	f2, axn = plt.subplots(nrow, ncol, figsize=(unit_x*ncol, unit_y*nrow))
	for p_id in range(top_pc):
		b_bias = np.reshape(U[:, p_id], (num_bin, num_bin))
		sns.heatmap(get_pivot2(np.transpose(b_bias)), annot=False, fmt=".2f", ax=axn.flat[p_id])
	f2.savefig(out_file)

if __name__=="__main__":
	directory = "hmrfem.whole.brain.e.fd0-48.correlated.gene"
	hippo_FDs = [30,31,32,33,34,35,36,37,38,39,40,41,42]
	cortex_FDs = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
	temporal_cortex_FDs = [20,21,22,23,24,25,26,27,28,29]
	roi = "whole.brain.e"

	#FDs = hippo_FDs + cortex_FDs + temporal_cortex_FDs
	FDs = hippo_FDs + cortex_FDs
	workdir = "/home/qz64/hmrf.submit"
	genes = reader.read_genes("%s/%s/genes" % (workdir, directory))
	Xcen, field = reader.read_coord("%s/%s/f%s.coordinates.2.txt" % (workdir, directory, roi)) #note the stitched version use the .2 version

	expr = np.empty((len(genes), Xcen.shape[0]), dtype="float32")
	for ind,g in enumerate(genes):
		expr[ind,:] = reader.read_expression("%s/%s/f%s.gene.%s.txt" % (workdir, directory, roi, g))
	
	expr_bias = np.empty((len(genes), 50*50), dtype="float32")
	for ind,g in enumerate(genes):
		bins = calc_bias_moving(expr=expr[ind,:], centroid=Xcen, field=field, interest_field=FDs, num_bin=50)
		expr_bias[ind,:] = np.ndarray.flatten(bins)

	corrected_expr = do_pca(expr=expr, expr_bias=expr_bias, centroid=Xcen, field=field, interest_field=FDs, num_bin=50, top_comp_remove=5)

	plot_pca(expr_bias=expr_bias, num_bin=50, top_pc=5, out_file="bias_component.pdf")

		
	if not os.path.isdir("%s/%s/bias_corrected" % (workdir,directory)):
		os.mkdir("%s/%s/bias_corrected" % (workdir, directory))
	
	for ind,g in enumerate(genes):
		print "Doing", g
		reader.write_expression(corrected_expr[ind,:], "%s/%s/bias_corrected/f%s.gene.%s.txt" % (workdir, directory, roi, g))
	
