from . import amiraparsing as ap
import numpy as np

## Switches the vertex coordinate data 
## Keeps the triangle information (connectivity)


def bodyChunk(bodyNum, body, i_type):
	bodyChunk=""
	for t in range(len(body[:])):
		lineChunk =""
		for q in range(len(body[t][:])):
			lineChunk += str(body[t][q]) + " "
		bodyChunk += "	"+ lineChunk + "\n"
	
	#bodyChunk = "Vertices "+str(bodyNum)+ "\n" + bodyChunk

	bodyChunk = i_type + " "+str(bodyNum)+ "\n" + bodyChunk

	return bodyChunk

def bodyChunk_f(bodyNum, body):
	bodyChunk=""
	for t in range(len(body[:])):
		lineChunk =""
		for q in range(len(body[t][:])):
			lineChunk += str(body[t][q]) + " "
		bodyChunk += "	"+ lineChunk + "\n"
	
	bodyChunk = "Vertices "+str(bodyNum)+ "\n" + bodyChunk
	return bodyChunk

def writeSurface_with_format(formatFile, outputFile, ptAr):
	format_list = ap.amiraParsingSurfaceExceptVertex(formatFile)
	vertexnum = len(ptAr)

	head = format_list[0]
	body = bodyChunk_f(vertexnum, ptAr)
	tail = format_list[1] + format_list[2] + format_list[3] + '\n'

	out_file = open(outputFile, "w")
	out_file.write(head+body+tail)
	out_file.close()

def writeSurface(outputFile, ptAr, tris):
	intro = "# HyperSurface 0.1 ASCII \n\n"
	vertexnum = len(ptAr)
	trisnum = len(tris)

	pt1 = bodyChunk(vertexnum, ptAr, "Vertices")
	interlude = "\n\nNBranchingPoints 0 \nNVerticesOnCurves 0 \nBoundaryCurves 0\nPatches 1\n{\nInnerRegion Pia\nOuterRegion Exterior\nBoundaryID 0\nBranchingPoints 0\n\n"
	pt2 = bodyChunk(trisnum, tris, "Triangles") +'\n' + '}' +'\n'

	whole = intro + pt1 + interlude + pt2

	out_file = open(outputFile, "w")
	out_file.write(whole)
	out_file.close()

## DEBUG
# directory = '/Users/peterpark/Library/Mobile Documents/com~apple~CloudDocs/Work/Image_processing_scripts/Tangential/TangentialData/'
# format_file = 'output_dec14_2.am_mc_vtk_simplified.surf'
# input1 = directory + format_file 
# #test = ap.amiraParsingSurfaceExceptVertex(input1)
# #params = ap.amiraParsingParameters(input1)
# #print test
# #print len(test)
# #print test[3]
# sf1 = ap.amiraParsingSurface2(input1)
# ptAr_surface = np.asarray(ap.convertToFloat(sf1[0]))

# writeSurface(input1, 'test_surface.txt', ptAr_surface)
# print "DONE"

