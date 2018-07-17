import os
import mdtraj as md
import glob
import numpy as np

from macros import *

def funcCreateSasaBenchmarkFile():
	f=open(sasa_benchmark_filename,"wb")
	f.writelines([
	"ALA\t129\n",
	"ARG\t274\n",
	"ASN\t195\n",
	"ASP\t193\n",
	"CYS\t167\n",
	"GLU\t223\n",
	"GLN\t225\n",
	"GLY\t104\n",
	"HIS\t224\n",
	"ILE\t197\n",
	"LEU\t201\n",
	"LYS\t236\n",
	"MET\t224\n",
	"PHE\t240\n",
	"PRO\t159\n",
	"SER\t155\n",
	"THR\t172\n",
	"TRP\t285\n",
	"TYR\t263\n",
	"VAL\t174\n"
	])
	f.close()

def funcExposedResidues(inpath,outpath,trajtype,top,subsample,cutoff):

	f_log=open(exposed_residues_logfilename,"wb")

	f_log.write("Writing "+sasa_benchmark_filename+" \n")
	funcCreateSasaBenchmarkFile()
	
	edit_benchmarks_flag=raw_input("Do you want to edit "+sasa_benchmark_filename+", Y or N \n")

	if edit_benchmarks_flag=="Y" or edit_benchmarks_flag=="":
		cmd="vi "+sasa_benchmark_filename
		os.system(cmd)

	outfolder=outpath+"/"+exposed_residues_sasa_featurization_foldername
	if os.path.isdir(outfolder) == False:
		cmd="mkdir "+outfolder
		os.system(cmd)

	first_traj_flag=0
	for file in sorted(glob.glob(inpath+'/*'+trajtype)):

		f_log.write("Reading "+file+" ...\n")
		t=md.load(file,top=top)[::subsample]

		if first_traj_flag==0:
			first_traj_flag=1
			R=t.topology.n_residues
			f_log.write("This protein has "+str(R)+" residues. \n")

			atom_numbers_by_residue=[]
			for i in range(R):
				r=t.topology.select('resid '+str(i))
				atom_numbers_by_residue.append(r)

		sasa=md.shrake_rupley(t)
		f_log.write("Featurizing trajectory based on sasa for every atom ...\n")
		outfile=outfolder+"/"+file.replace(inpath,"",1)+".npy"
		np.save(outfile,sasa)
		break

	for file in sorted(glob.glob(outfolder+'/*')):
		print file
		a=np.load(file)
		sasa_all_res=[]
		for i in range(len(atom_numbers_by_residue)):
			sasa_traj=[]
			for j in range(len(a)):
				sasa=0
				for k in atom_numbers_by_residue[i]:
					sasa=sasa+a[j][k]
				sasa_traj.append(sasa*100)
			sasa_all_res.append(sasa_traj)
		outfile=outfolder+"/"+file.split('/')[-1]+'_sasa_by_res.npy'
		print outfile
		np.save(outfile,sasa_all_res)
	
	dataset=[]
	for file in sorted(glob.glob(outfolder+'/*sasa_by_res.npy')):
		a=np.load(file)
		dataset.append(a)

	f_log.close()
