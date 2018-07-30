import numpy as np
import math
import sys
import random
#import matplotlib.pyplot as plt

def choose_random_cells(n, k):
	X = read_expression_matrix(n)
	ncell = X.shape[0]
	allcell = [x for x in range(ncell)]
	random.shuffle(allcell)
	ngene = X.shape[1]
	for i in range(k):
		sys.stdout.write("%d " % (i+1))
		for g in range(ngene):
			sys.stdout.write("%.5f" % X[allcell[i], g])
			if g==ngene-1:
				sys.stdout.write("\n")
			else:
				sys.stdout.write(" ")
	
def read_adjacency(n):
	f = open(n)
	m = {}
	for l in f:
		l = l.rstrip("\n").split(" ")
		pt = int(l[0])
		m.setdefault(pt, [])
		for j in l[1:]:
			if j=="-1":
				break
			m[pt].append(int(j))
	f.close()
	return m

def read_genes(n):
	f = open(n)
	genes = []
	for l in f:
		l = l.rstrip("\n")
		genes.append(l)
	f.close()
	return genes
	
def read_coord(n):
	f = open(n)
	m = {}
	field = 10
	for l in f:
		l = l.rstrip("\n").split(" ")
		pt = l[0]
		field = int(l[1])
		coord1 = float(l[2])
		coord2 = float(l[3])
		m[pt] = (field, coord1, coord2)
	f.close()
	ma = np.empty((len(m)+1, 2))
	ma[0] = [0, 0]
	field = np.arange(len(m)+1)
	field[0] = 0
	for k in m:
		ma[int(k)] = (m[k][1], m[k][2])
		field[int(k)] = m[k][0]
	return ma, field
	
#def read_classes(n, plot=False):
def read_classes(n):
	f = open(n)
	m = {}
	prob = []
	for l in f:
		l = l.rstrip("\n").split(" ")
		pt = l[0]
		cc = [float(e) for e in l[1:]]
		cl = np.argmax(cc) + 1
		prob.append(max(cc))
		m[pt] = cl
	f.close()
	ma = np.arange(len(m)+1)
	ma[0] = -1
	for k in m:
		ma[int(k)] = m[k]
	count0_05 = len([x for x in prob if 1-x>0.05])
	count0_01 = len([x for x in prob if 1-x>0.01])
	count0_2 = len([x for x in prob if 1-x>0.2])
	#count0.01 = 
	#count0.005 = 
	#count0.001 = 
	#print ["%.2e" % x for x in prob]
	#print count0_05, count0_01, count0_2

	#if plot:
	#	plt.hist(np.array(prob), bins=100, histtype="step")

	return ma
	
def read_cell_type(n):
	f = open(n)
	m = {}
	labels = set([])
	for l in f:
		l = l.rstrip("\n").split("\t")
		pt = l[0]
		m[int(pt)] = l[1]
		labels.add(l[1])
	f.close()

	dx = int(len(labels)/2)
	di = -1 * dx
	sort_labels = list(sorted(labels))

	label_pos = {}
	for i,s in enumerate(sort_labels):
		label_pos[s] = i
		
	s_labels = set(labels)
	print s_labels
	
	'''
	if "Glutamatergic Neuron" in s_labels and \
	"Endothelial Cell" in s_labels:
		tmp1 = label_pos["Glutamatergic Neuron"]
		tmp2 = label_pos["Endothelial Cell"]
		sort_labels[tmp1] = "Endothelial Cell"
		sort_labels[tmp2] = "Glutamatergic Neuron"
		label_pos["Glutamatergic Neuron"] = tmp2
		label_pos["Endothelial Cell"] = tmp1		
	
	if "Astrocyte" in s_labels and \
	"Endothelial Cell" in s_labels:
		tmp1 = label_pos["Astrocyte"]
		tmp2 = label_pos["Endothelial Cell"]
		sort_labels[tmp1] = "Endothelial Cell"
		sort_labels[tmp2] = "Astrocyte"
		label_pos["Astrocyte"] = tmp2
		label_pos["Endothelial Cell"] = tmp1	
	'''
	'''
	if "GABA-ergic Neuron" in s_labels and \
	"Glutamatergic Neuron" in s_labels and \
	"Oligodendrocyte" in s_labels:
		tmp1 = label_pos["GABA-ergic Neuron"]
		#tmp2 = label_pos["Glutamatergic Neuron"]
		tmp3 = label_pos["Oligodendrocyte"]
		sort_labels[tmp1] = "Oligodendrocyte"
		sort_labels[tmp3] = "GABA-ergic Neuron"
		#sort_labels[tmp2] = "Oligodendrocyte.3"
		#sort_labels[tmp4] = "Glutamatergic Neuron"
	'''
	dd = {}
	for s in sort_labels:
		if di==0:
			di+=1
		dd[s] = di
		di+=1
		
	ma = np.arange(len(m.keys())+1)
	ma[0] = -1
	for k in sorted(m.keys()):
		ma[k] = dd[m[k]]
	print sort_labels
	return ma, dd

def get_likelihood(n): #need unnormprob files
	'''
	w = {}
	tot_w = 0
	f = open(n)
	for l in f:
		l = l.rstrip("\n").split(" ")
		cc = [float(e) for e in l[1:]]
		cl = np.argmax(cc) + 1
		w.setdefault(cl, 0)
		w[cl]+=1
		tot_w+=1
	f.close()
	for wi in w:
		w[wi] = w[wi] / float(tot_w)
	'''
	
	f = open(n)
	prob = {}
	tot = 0
	for l in f:
		l = l.rstrip("\n").split(" ")
		cc = [float(e) for e in l[1:]]
		num_val = len(cc)
		tot_density = 0
		for i,j in zip(range(1,num_val+1), cc):
			tot_density += j
		this_prob = {}
		for i,j in zip(range(1,num_val+1), cc):
			this_prob[i] = j / tot_density
			prob.setdefault(i, 0)
			prob[i] += this_prob[i]
		tot+=1
	f.close()
	
	for i in prob:
		prob[i] = prob[i] / tot
		
	likelihood = 0
	f = open(n)
	for l in f:
		l = l.rstrip("\n").split(" ")
		cc = [float(e) for e in l[1:]]
		num_val = len(cc)
		this_like = 0
		for i,j in zip(range(1,num_val+1), cc):
			this_like += prob[i] * j
		likelihood+=math.log(this_like)
	f.close()
	likelihood /= tot
	return likelihood, tot
	
def read_clusters(n):
	f = open(n)
	m = {}
	for l in f:
		l = l.rstrip("\n").split(" ")
		pt = l[0]
		clust = int(l[1])
		m[pt] = clust
	f.close()
	ma = np.arange(len(m)+1)
	ma[0] = -1
	for k in m:
		ma[int(k)] = m[k]
	return ma
	
def read_kmeans(n):
	f = open(n)
	m = {}
	for l in f:
		l = l.rstrip("\n").split(" ")
		pt = l[0]
		cl = int(l[1])
		m[pt] = cl
	f.close()
	ma = np.arange(len(m)+1)
	ma[0] = -1
	for k in m:
		ma[int(k)] = m[k]
	return ma
	
def read_expression(n):
	f = open(n)
	m = {}
	for l in f:
		l = l.rstrip("\n").split(" ")
		pt = l[0]
		m[pt] = float(l[1])
	f.close()
	ma = np.arange(len(m)+1, dtype="float32")
	ma[0] = -1
	for k in m:
		ma[int(k)] = m[k]
	return ma

def read_expression_matrix(n):
	X = np.loadtxt(n, dtype="float32")
	X = X[:, 1:]
	return X

def write_expression(x, fileName):
	fw = open(fileName, "w")
	for i in range(1, x.shape[0]):
		fw.write("%d %.5f\n" % (i, x[i]))
	fw.close()

def write_expression_matrix(x, fileName):
	fw = open(fileName, "w")
	for i in range(x.shape[0]):
		fw.write("%d " % (i+1))
		for j in range(x.shape[1]):
			fw.write("%.2f" % (x[i,j]))
			if j==x.shape[1]-1:
				fw.write("\n")
			else:
				fw.write(" ")
	fw.close()

def write_coordinate(Xcen, field, fileName):
	fw = open(fileName, "w")
	for i in range(1, field.shape[0]):
		fw.write("%d %d %.5f %.5f\n" % (i, field[i], Xcen[i,0], Xcen[i,1]))
	fw.close()
	
