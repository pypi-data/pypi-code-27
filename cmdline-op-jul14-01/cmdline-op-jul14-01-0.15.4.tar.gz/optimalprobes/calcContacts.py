import mdtraj as md
import os
import glob
import numpy as np

from macros import *

def funcContactList(R,ter):
	cont=[]
	if ter==False:
		start=0
		end=R
	else:
		start=1
		end=R-1
	for i in range(start, end):
		for j in range(i+1,end):
			temp_list=[]
			temp_list.append(i)
			temp_list.append(j)
			cont.append(temp_list)
	return cont


def funcCalcContacts(inpath,outpath,trajtype,top,scheme,subsample,ter):

	f_log=open(calc_contacts_logfilename,"wb")

	outfolder=outpath+"/"+calc_contacts_all_contact_featurization_foldername
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
			cont=funcContactList(R,ter)
			f_log.write("Proceeding to compute "+str(len(cont))+" contacts. \n")

		dist=md.compute_contacts(t,cont,scheme=scheme)
		f_log.write("Featurizing trajectory based on all contacts ...\n")
		ftr=[np.ndarray.tolist(dist[0][i][:]) for i in range(len(dist[0]))]
		outfile=outfolder+"/"+file.replace(inpath,"",1)+".npy"
		np.save(outfile, ftr)

	f_log.close()
