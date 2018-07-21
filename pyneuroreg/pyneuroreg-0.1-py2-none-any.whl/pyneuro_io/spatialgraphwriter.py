'''
General spatial graph writer 

Written by Peter Park 
'''
from . import amiraparsing as ap
import numpy as np
import pyneuro_autoalign.autoalign as aa

versionNum = 0.54 # March 6. 2018

## NOTE:
# The height_adjustment translation was corrected to a positive offset. 

## Helper Function
def process_file(input_file):
	numContourStr = ap.amiraParsingIndex(input_file,'4')
	numContourLs = ap.convertToInt(numContourStr)
	ct_grouping = [ numContourLs[i][0]for i in range(0, len(numContourLs))]
	
	EdgePts = ap.amiraParsingIndex(input_file,'6')
	EdgePtsFL = ap.convertToFloat(EdgePts)
	ptAr = np.array(EdgePtsFL)
	
	return ct_grouping, ptAr


def bodyChunk(bodyNum, body):
	bodyChunk=""
	for t in range(len(body[:])):
		lineChunk =""
		for q in range(len(body[t][:])):
			lineChunk += str(body[t][q]) + " "
		bodyChunk += lineChunk + "\n"
	
	bodyChunk = "@"+str(bodyNum)+ "\n" + bodyChunk + "\n"
	return bodyChunk


### Generic Version: you need to specify each data section.  
def writeSpatialGraph(formatFile, outputFile, bodylist):
	head = ap.amiraParsingHeader(formatFile)
	dataSecMsg = "# Data section follows" + "\n"
	body1 = bodyChunk(1, bodylist[0])
	body2 = bodyChunk(2, bodylist[1])
	body3 = bodyChunk(3, bodylist[2])
	body4 = bodyChunk(4, bodylist[3])
	body5 = bodyChunk(5, bodylist[4])
	body6 = bodyChunk(6, bodylist[5])
	body7 = bodyChunk(7, bodylist[6])

	valueBody = "".join([body1, body2, body3, body4, body5, body6, body7])

	wholeBody = dataSecMsg +"\n" + valueBody

	test_file = open(outputFile, "w")
	test_file.write(head+wholeBody)
	test_file.close() 

# A specific graph-writing function for coronal alignment 
# VertexCoordinates and EdgePOintCoordinates are to be replaced from those in the format file. 
def writeCoronalSpatialGraph(formatFile, outputFile, ptAr, transformation_list):
	head = ap.amiraParsingHeader(formatFile)

	## Copying from the format file 
	body2_ptAr = ap.amiraParsingIndex(formatFile, 2)
	body2 = bodyChunk(2, body2_ptAr)

	body3_ptAr = ap.amiraParsingIndex(formatFile, 3)
	body3 = bodyChunk(3, body3_ptAr)

	body4_ptAr = ap.amiraParsingIndex(formatFile, 4)
	body4 = bodyChunk(4, body4_ptAr)

	body5_ptAr = ap.amiraParsingIndex(formatFile, 5)
	body5 = bodyChunk(5, body5_ptAr)

	body7_ptAr = ap.amiraParsingIndex(formatFile, 7)
	body7 = bodyChunk(7, body7_ptAr)

	dataSecMsg = "# Data section follows" + "\n"

	## Replacing with newly generated values 
	body1_ptAr_raw = ap.amiraParsingIndex(formatFile, 1)
	body1_ptAr = np.asarray(ap.convertToFloat(body1_ptAr_raw))

	turning = transformation_list[0]
	translation1 = transformation_list[1]
	translation2 = transformation_list[2]

	body1_ptAr[:,:2] = aa.rotate(body1_ptAr[:,:2], turning)
	body1_ptAr[:,:2] = aa.translate(body1_ptAr[:,:2],translation1[0], translation1[1])
	body1_ptAr[:,:2] = aa.translate(body1_ptAr[:,:2], 0, translation2)
	body1_ptAr[:,2] = ptAr[:,2][0]

	body1 = bodyChunk(1, body1_ptAr)

	body6 = bodyChunk(6, ptAr)
	
	valueBody = "".join([body1, body2, body3, body4, body5, body6, body7])

	wholeBody = dataSecMsg + valueBody

	test_file = open(outputFile, "w")
	test_file.write(head+wholeBody)
	test_file.close() 


# A specific graph-writing fuction for Blood Vessel Vectors 
def writeVectorGraph(formatFile, outputFile, vectorlabel, vectorList):
	params = ap.amiraParsingParameters(formatFile)

	connectList = []
	for i in range(len(vectorList)/2):
		t = i*2
		connectList.append(np.array([t,t+1]))

	# for i in range(len(vectorList):
	# 	for q in range(len(vectorList[0][:])):
	# 	vectorList[i][q] =

	## Must change the print type to a scientific form for amira
	# this changes data type of each element of vectorList (from np.array to list)
	# for q in range(len(vectorList[:])):
	# 	dummylist = []
	# 	for w in range(len(vectorList[q][:])):
	# 		dummylist.append(convertToScientificForm(vectorList[q][w]))
	# 	vectorList[q] = dummylist

	b1 = vectorList
	b2 = [[vectorlabel] for i in range(len(vectorList))]
	b3 = [(str(connectList[i][0]), str(connectList[i][1])) for i in range(len(connectList))]
	b4 = [[2] for i in range(len(connectList))] # since two dots form a line
	b5 = [[vectorlabel] for i in range(len(connectList))]
	b6 = vectorList
	b7 = [[3.079110145568848e+000] for i in range(len(vectorList))]

	body1 = bodyChunk(1, b1)
	body2 = bodyChunk(2, b2)
	body3 = bodyChunk(3, b3)
	body4 = bodyChunk(4, b4)
	body5 = bodyChunk(5, b5)
	body6 = bodyChunk(6, b6)
	body7 = bodyChunk(7, b7)

	valueBody = "".join([body1, body2, body3, body4, body5, body6, body7])
	dataSecMsg = "# Data section follows"
	wholeBody = dataSecMsg +"\n" + valueBody


	firstLine = "# AmiraMesh 3D ASCII 2.0\n\n\n"

	vertex = "define VERTEX "+ str(len(vectorList)) + "\n"
	edge = "define EDGE " + str(len(connectList)) + "\n"
	point = "define POINT " + str(len(vectorList)) + "\n"

	head = firstLine + vertex + edge + point + params
	out_file = open(outputFile, "w")
	out_file.write(head+wholeBody)
	out_file.close()

# Debug

print "Spatial Graph Writer Version: " + str(versionNum)
# test1 = [[1,2,3],[4,5,6]]
# test2 = np.array([[9,10,11],[11,23,152]])
# test3 = [np.array([100,101,102]), np.array([511,521,122])]
# bodylist=[test1, test2, test3, 'test4', 'test5', 'test6', 'test7']
# sgw.writeSpatialGraph(input_file,"testbyfunction2.text", bodylist)

# directory = '/Users/peterpark/Library/Mobile Documents/com~apple~CloudDocs/Work/Image_processing_scripts/Tangential/TangentialData/'
# file1 = 'WR49_only_BVs_manual_detect_labeled_post-pruning.am'
# input1 = directory + file1 
# generateVectorField(input1, "projection.am", 10, vectorList)


