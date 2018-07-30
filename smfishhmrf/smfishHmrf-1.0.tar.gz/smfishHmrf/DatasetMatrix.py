import sys
import math
import os
import numpy as np
import scipy
import scipy.stats
import random
from scipy.stats import zscore
from scipy.spatial.distance import euclidean,squareform,pdist
sys.setrecursionlimit(10000)

class DatasetMatrix:
	expr = None
	Xcen = None
	genes = []
	cells = []
	ngene = 0
	ncell = 0
	edges = None
	adjacent = None
	blocks = None
	cutoff = 0

	def __init__(self, expr, genes, cells, Xcen):
		self.expr = expr
		self.genes = genes
		self.cells = cells
		self.Xcen = Xcen
		self.ngene = len(genes)
		self.ncell = Xcen.shape[0]

	def get_adjacency_list(self, dist=None, cutoff=None):
		ncell = dist.shape[0]
		points = set([])
		edges = set([])
		adjacent = {}
		for i in range(ncell):
			for j in range(i+1, ncell):
				if dist[i,j]<=cutoff:
					edges.add(tuple(sorted([i, j])))
					points = points | set([i,j])
		for i in range(ncell):
			if i in points: continue
			dist_i = sorted([(dist[i,j], j) for j in range(ncell) if i!=j])
			edges.add(tuple(sorted([i, dist_i[0][1]])))
		for e1, e2 in edges:
			adjacent.setdefault(e1, set([]))
			adjacent.setdefault(e2, set([]))
			adjacent[e1].add(e2)
			adjacent[e2].add(e1)
		return edges, adjacent
	
	def test_adjacency_list(self, percentages, metric="euclidean"):
		percentile = {}
		dist = pdist(self.Xcen, metric=metric)
		s_dist = squareform(dist)
		for px in percentages:
			percentile[px] = np.percentile(dist, px)
			edges, adjacent = self.get_adjacency_list(dist=s_dist, cutoff=percentile[px])
			avg_neighbor = np.mean([len(adjacent[n]) for n in adjacent])
			print "cutoff:%.2f%%" % px, "#nodes:%d" % len(adjacent), \
			"#edges:%d"%len(edges), "avg.nei:%.2f" % avg_neighbor
	
	def calc_neighbor_graph(self, cutoff, metric="euclidean"):
		dist = pdist(self.Xcen, metric=metric)
		s_dist = squareform(dist)
		self.cutoff = cutoff
		percent_value = np.percentile(dist, self.cutoff)
		self.edges, self.adjacent = self.get_adjacency_list(dist=s_dist, cutoff=percent_value)
	
	def write_neighbor_graph(self, adj_file=None, edge_file=None):
		print "Adjacency"
		maxNeighbor = max([len(self.adjacent[e]) for e in self.adjacent.keys()])
		fw = open(adj_file, "w")
		for i in range(self.ncell):
			numPad = maxNeighbor - len(self.adjacent[i])
			ix = [(e+1) for e in sorted(self.adjacent[i])]
			ix.extend([-1 for iv in range(numPad)])
			fw.write("%d " % (i+1) + " ".join(["%d" % e for e in ix]) + "\n")
		fw.close()
		print "Edges"
		fw = open(edge_file, "w")
		for e1, e2 in self.edges:
			fw.write("%d %d\n" % (e1+1, e2+1))
		fw.close()

	def calc_independent_region(self):
		edge_file = "/tmp/edges.txt"
		block_file = "/tmp/blocks.txt"
		adj_file = "/tmp/adjacent.txt"
		self.write_neighbor_graph(adj_file=adj_file, edge_file=edge_file)
		os.system("java -cp /home/qz64/hmrf.submit/graphColoring/code GraphColoring %s %s" % (edge_file, block_file))
		self.blocks = []
		f = open(block_file)
		for l in f:
			l = l.rstrip("\n")
			ll = l.split()
			self.blocks.append(int(ll[1]))
		f.close()
		self.blocks = np.array(self.blocks)

	def write_blocks(self, outfile):
		fw = open(outfile, "w")
		for i in range(self.blocks.shape[0]):
			fw.write("%d %d\n" % (i+1, self.blocks[i]))
		fw.close()

	def write_genes(self, outfile):
		fw = open(outfile, "w")
		for g in self.genes:
			fw.write(g + "\n")
		fw.close()
	
	def write_expression(self, outfile):
		fw = open(outfile, "w")
		for ic in range(self.ncell):	
			fw.write("%d " % (ic+1) + " ".join(["%.2f" % self.expr[j,ic] for j in range(self.ngene)]) + "\n")
		fw.close()
	
	def write_coordinates(self, outfile):
		fw = open(outfile, "w")
		for ic in range(self.ncell):
			fw.write("%d %d %.3f %.3f\n" % (ic+1, 0, self.Xcen[ic, 0], self.Xcen[ic, 1]))
		fw.close()

	def subset_genes(self, custom_genes):
		ind = np.array([self.genes.index(g) for g in custom_genes if g in set(self.genes)])
		new_expr = self.expr.copy()
		new_expr = new_expr[ind, :]
		new_dset = DatasetMatrix(new_expr, custom_genes, self.cells, self.Xcen)
		new_dset.edges = self.edges
		new_dset.adjacent = self.adjacent
		new_dset.blocks = self.blocks
		new_dset.cutoff = self.cutoff
		return new_dset

	def shuffle(self, shuffle_prop):
		new_expr = np.transpose(self.expr)
		row_order = np.empty((self.ncell), dtype="int32")
		for i in range(self.ncell):
			row_order[i] = i

		per = shuffle_prop
		#per = 0.99 #0.05, 0.10, 0.20, 0.50, 0.99
		shuf_cutoff = int(float(self.ncell) * per)
		row_order_copy = np.copy(row_order)
	
		ig = 0
		while True:
			this_sample = random.sample(range(0, self.ncell), 2)
			tmp = row_order_copy[this_sample[0]]
			row_order_copy[this_sample[0]] = row_order_copy[this_sample[1]]
			row_order_copy[this_sample[1]] = tmp
			num_changed = 0
			for i in range(self.ncell):
				if row_order_copy[i]!=row_order[i]:
					num_changed+=1
			if num_changed>shuf_cutoff:
				break
			ig +=1
	
		new_expr = new_expr[row_order_copy, :]
		new_expr = np.transpose(new_expr)

		new_dset = DatasetMatrix(new_expr, self.genes, self.cells, self.Xcen)
		new_dset.edges = self.edges
		new_dset.adjacent = self.adjacent
		new_dset.blocks = self.blocks
		new_dset.cutoff = self.cutoff

		return new_dset		
