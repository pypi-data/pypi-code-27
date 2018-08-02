import re
import sys
import os
import numpy as np
import math
from scipy.spatial.distance import squareform, pdist
import smfishHmrf.reader as reader
from smfishHmrf.DatasetMatrix import DatasetMatrix, DatasetMatrixSingleField

class HMRFInstance:
	dest = ""
	prefix = ""
	dataset = None #must be DatasetMatrix
	beta_incr = 0
	start_beta = 0
	num_beta = 0
	tolerance = 1e-60
	k = []
	nstart = 1000
	likelihood = {}
	domain = {}

	def prepare(self):
		self.dataset.write_neighbor_graph(adj_file="%s/f%s.adjacency.txt" % (self.dest, self.prefix), \
		edge_file="%s/f%s.edges.txt" % (self.dest, self.prefix))
		self.dataset.write_coordinates("%s/f%s.coordinates.txt" % (self.dest, self.prefix))
		self.dataset.write_blocks("%s/f%s.blocks.txt" % (self.dest, self.prefix))
		self.dataset.write_genes("%s/genes" % self.dest)
		self.dataset.write_expression("%s/f%s.expression.txt" % (self.dest, self.prefix))

		fw = open("%s/generateCentroids.multi.R" % self.dest, "w")
		fw.write("""par_k <- commandArgs(trailingOnly = TRUE)[1]
nstart <- commandArgs(trailingOnly = TRUE)[2]
mem_file <- commandArgs(trailingOnly = TRUE)[3]
centroid_file <- commandArgs(trailingOnly = TRUE)[4]
kmeans_file <- commandArgs(trailingOnly = TRUE)[5]

par_k <- as.integer(par_k)
nstart <- as.integer(nstart)
y<-read.table(mem_file, header=F, row.names=1)
y<-as.matrix(y)
k<-par_k
m<-dim(y)[2]
kk<-kmeans(y, k, nstart=nstart, iter.max=100)

write.table(kk$cluster, file=kmeans_file, sep=" ", quote=F, col.names=F, row.names=T)
write.table(kk$centers, file=centroid_file, sep=" ", quote=F, col.names=F, row.names=T)
		""")
		fw.close()

		fw = open("%s/getHMRFEM.multi.beta.auto.R" % self.dest, "w")
		fw.write("""library(dplyr)
library(smfishHmrf)
print("Loaded smfishHmrf")
mem_file <- commandArgs(trailingOnly = TRUE)[1]
nei_file <- commandArgs(trailingOnly = TRUE)[2]
block_file <- commandArgs(trailingOnly = TRUE)[3]
centroid_file <- commandArgs(trailingOnly = TRUE)[4]
beta <- commandArgs(trailingOnly = TRUE)[5]
beta_increment <- commandArgs(trailingOnly = TRUE)[6]
beta_num_iter <- commandArgs(trailingOnly = TRUE)[7]
par_k <- commandArgs(trailingOnly = TRUE)[8]
outdir <- commandArgs(trailingOnly = TRUE)[9]
prefix <- commandArgs(trailingOnly = TRUE)[10]
tolerance <- commandArgs(trailingOnly = TRUE)[11]

beta<-as.double(beta)
beta_increment<-as.double(beta_increment)
beta_num_iter<-as.integer(beta_num_iter)
par_k <- as.integer(par_k)
tolerance <- as.double(tolerance)

#file reading
y<-read.table(mem_file, header=F, row.names=1)
y<-as.matrix(y)
nei<-read.table(nei_file, header=F, row.names=1)
colnames(nei)<-NULL
rownames(nei)<-NULL
nei<-as.matrix(nei)
blocks<-read.table(block_file, header=F, row.names=1)
blocks<-c(t(blocks))
maxblock <- max(blocks)
blocks<-lapply(1:maxblock, function(x) which(blocks == x))
numnei<-apply(nei, 1, function(x) sum(x!=-1))
centroid<-read.table(centroid_file, header=F, row.names=1)
centroid<-as.matrix(centroid)
#parameter setting
k<-par_k
m<-dim(y)[2]
sigma <-array(0, c(m,m,k))
for(i in 1:k){
	sigma[, ,i] <- cov(y)
	print(rcond(sigma[,,i]))
}
mu<-array(0, c(m,k))
kk2<-centroid
for(i in 1:k){
	mu[,i] <- kk2[i,]
}
numcell<-dim(y)[1]
kk_dist<-array(0, c(numcell, k))
for(i in 1:numcell){
	for(j in 1:k){
		kk_dist[i,j] <- dist(rbind(y[i,], mu[,j]), method="euclidean")
	}
}
clust_mem<-apply(kk_dist, 1, function(x) which(x==min(x))) 
lclust<-lapply(1:k, function(x) which(clust_mem == x))
damp<-array(0, c(k))
for(i in 1:k){
	sigma[, , i] <- cov(y[lclust[[i]], ])
	#default tolerance is 1e-60
	di<-findDampFactor(sigma[,,i], factor=1.05, d_cutoff=tolerance, startValue=0.0001)
    if(is.null(di)){
        damp[i] = 0
    }else{
        damp[i] = di
    }
}

#needs y, nei, beta, numnei, blocks, mu, sigma, damp
do_one <- function(prefix, outdir, #all strings
                   par_k, par_y, par_nei, par_beta, par_numnei, par_blocks, 
                   par_mu, par_sigma, par_damp){ #beta is double, par_k is integer

out_file <- sprintf("%s/%s.%.1f.prob.txt", outdir, prefix, par_beta) #hmrfem probability
out_file_2 <- sprintf("%s/%s.%.1f.centroid.txt", outdir, prefix, par_beta) #hmrfem centroids
out_file_3 <- sprintf("%s/%s.%.1f.hmrf.covariance.txt", outdir, prefix, par_beta) #hmrfem covariance
out_file_unnorm <- gsub("prob", "unnormprob", out_file)

tc.hmrfem<-smfishHmrf.hmrfem.multi(y=par_y, neighbors=par_nei, beta=par_beta, numnei=par_numnei, 
blocks=par_blocks, mu=par_mu, sigma=par_sigma, verbose=T, 
err=1e-7, maxit=50, dampFactor=par_damp)

write.table(tc.hmrfem$prob, file=out_file, sep=" ", quote=F, col.names=F, row.names=T)
write.table(tc.hmrfem$unnormprob, file=out_file_unnorm, sep=" ", quote=F, col.names=F, row.names=T)
write.table(t(tc.hmrfem$mu), file=out_file_2, sep=" ", quote=F, col.names=F, row.names=T)
write.table(tc.hmrfem$sigma[,,1], file=out_file_3, sep=" ", quote=F, col.names=F, row.names=T)
for(i in 2:par_k){
	write.table(tc.hmrfem$sigma[,,i], file=out_file_3, sep=" ", quote=F, col.names=F, row.names=T, append=T)
}
}

beta_current <- beta
for(bx in 1:beta_num_iter){
	print(sprintf("%.3f", beta_current))
	do_one(prefix, outdir, k, y, nei, beta_current, numnei, blocks, mu, sigma, damp)
	beta_current <- beta_current + beta_increment
}
	""")
		fw.close()

		os.system("chmod a+x %s/generateCentroids.multi.R" % self.dest)
		os.system("chmod a+x %s/getHMRFEM.multi.beta.auto.R" % self.dest)

	def __init__(self, prefix, dest, dataset, k, start_beta, beta_incr, num_beta, tolerance=1e-60):
		assert isinstance(dataset, DatasetMatrix), "dataset is not of DatasetMatrix"
		self.dest = dest
		self.tolerance = tolerance
		self.dataset = dataset
		self.prefix = prefix
		if isinstance(k, list):
			self.k = k
		else:
			self.k = [k,]
		self.start_beta = start_beta
		self.beta_incr = beta_incr
		self.num_beta = num_beta
		self.prepare()

	def init(self, nstart=1000):
		self.nstart = nstart
		cur = os.getcwd()
		os.chdir(self.dest)
		#input file (need to generate)
		expr_file = "f%s.expression.txt" % self.prefix

		for t_k in self.k:
			o_dir = "k_%d" % t_k
			if not os.path.isdir(o_dir):
				os.mkdir(o_dir)
			#output files
			centroid_file = "%s/f%s.gene.ALL.centroid.txt" % (o_dir, self.prefix)
			kmeans_file = "%s/f%s.gene.ALL.kmeans.txt" % (o_dir, self.prefix)
			os.system("Rscript generateCentroids.multi.R %d %d %s %s %s" % (t_k, self.nstart, expr_file, centroid_file, \
			kmeans_file))

		os.chdir(cur)

	def run(self):
		cur = os.getcwd()
		os.chdir(self.dest)
		adjacency_file = "f%s.adjacency.txt" % self.prefix
		block_file = "f%s.blocks.txt" % self.prefix
		expr_file = "f%s.expression.txt" % self.prefix
		for t_k in self.k:
			o_dir = "k_%d" % t_k
			centroid_file = "%s/f%s.gene.ALL.centroid.txt" % (o_dir, self.prefix)
			o_file_prefix = "f%s.beta" % self.prefix
			cmd = "Rscript getHMRFEM.multi.beta.auto.R %s %s %s %s %.1f %.1f %d %d %s %s %.1e" % (\
			expr_file, adjacency_file, block_file, centroid_file, self.start_beta, \
			self.beta_incr, self.num_beta, t_k, o_dir, o_file_prefix, self.tolerance)
			os.system(cmd)

		for t_k in self.k:
			o_dir = "k_%d" % t_k
			for t_b in range(self.num_beta):
				this_beta = self.start_beta + t_b * self.beta_incr
				lik, tot = reader.get_likelihood("%s/f%s.beta.%.1f.unnormprob.txt" % (o_dir, self.prefix, this_beta))
				self.likelihood[(t_k, this_beta)] = lik * tot
				self.domain[(t_k, this_beta)] = reader.read_classes("%s/f%s.beta.%.1f.prob.txt" % (o_dir, self.prefix, this_beta))[1:]

		os.chdir(cur)
	
	def plot_domain(self, this_k, this_beta, dot_size=45, lim=5000, size_factor=10, out_file=None):
		f, axn = plt.subplots(1, 1, figsize=(size_factor, size_factor), sharex=True, sharey=True)
		plt.subplots_adjust(hspace=0.01, wspace=0.01)
		cm = plt.cm.get_cmap("RdYlBu_r")
		cls = self.domain[(this_k, this_beta)]
		axn.scatter(self.Xcen[:,0], self.Xcen[:,1], s=dot_size, c=cls, edgecolors="gray", cmap=cm, vmin=1, vmax=max(cls))
		axn.set_xlim(0, lim)
		axn.set_ylim(-1 * lim, 0)
		f.savefig(out_file)
		
