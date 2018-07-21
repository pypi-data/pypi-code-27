from . import amiraparsing as ap
import numpy as np


def bodyChunk(bodyNum, body):
	bodyChunk=""
	for t in range(len(body[:])):
		lineChunk =""
		for q in range(len(body[t][:])):
			lineChunk += str(body[t][q]) + " "
		bodyChunk += lineChunk + "\n"
	
	bodyChunk = "@"+str(bodyNum)+ "\n" + bodyChunk + "\n"
	return bodyChunk


def writeLandmarkAscii(outputFile, ptAr):


	if len(np.shape(ptAr)) == 1: 
		landmark_num = 1
		body = str(ptAr[0]) + ' ' + str(ptAr[1]) + ' ' + str(ptAr[2]) + '\n'

	else:
		landmark_num = len(ptAr)
		body = bodyChunk(1, ptAr) # When dealing with multiple landmarks 


	firstLine = "# Avizo 3D ASCII 2.0\n\n\n"

	define = "define Markers "+ str(landmark_num) + "\n\n"

	block1 ='Parameters {\n    NumSets 1,\n    ContentType "LandmarkSet"\n} \n\n'
	block2 = 'Markers { float[3] Coordinates } @1\n\n'
	dataSecMsg = "# Data section follows" + "\n" 
	
	head = firstLine + define + block1 + block2 + dataSecMsg

	out_file = open(outputFile, "w")
	out_file.write(head+body)
	out_file.close()



def writeLandmarkAscii_single(outputFile, ptAr):
	firstLine = "# Avizo 3D ASCII 2.0\n\n\n"

	define = "define Markers "+ str(len(ptAr)) + "\n\n"

	block1 ='Parameters {\n    NumSets 1,\n    ContentType "LandmarkSet"\n} \n\n'
	block2 = 'Markers { float[3] Coordinates } @1\n\n'
	dataSecMsg = "# Data section follows" + "\n" 
	
	head = firstLine + define + block1 + block2 + dataSecMsg
	body = bodyChunk(1, ptAr)

	out_file = open(outputFile, "w")
	out_file.write(head+body)
	out_file.close()
