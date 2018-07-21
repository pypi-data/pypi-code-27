import pyneuro_io.amiraparsing as ap
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import math
import pickle 
from tqdm import tqdm_notebook as tqdm # if you want to run it in jupyter notebook


# edgePt_code: EdgePointCoordinates
# numEdge_code: NumEdgePoints
def process_file(input_file, numEdge_code, edgePt_code):
	numContourStr = ap.amiraParsingIndex(input_file, numEdge_code)
	numContourLs = ap.convertToInt(numContourStr)
	ct_grouping = [ numContourLs[i][0]for i in range(0, len(numContourLs))]
	
	EdgePts = ap.amiraParsingIndex(input_file, edgePt_code)
	EdgePtsFL = ap.convertToFloat(EdgePts)
	ptAr = np.array(EdgePtsFL)
	
	return ct_grouping, ptAr

def process_files_ptArList(files, numEdge_code, edgePt_code):
	ptAr_list = []
	for each_file in files:
		ct_gr, ptAr = process_file(each_file, numEdge_code, edgePt_code) 
		ptAr_list.append([ct_gr, ptAr])
	
	return ptAr_list 

def sg_plot(ct_grouping, ptAr, plot_now = False):
	
	contourDict = {}
	uniqueIndexHelper = []
	ptIndexHelper = [0]

	ContourIndex = [q for q in range(len(ct_grouping))]
	for i in range(len(ContourIndex)):
		for k in range(ct_grouping[i]): # this is the problem the index starts over everytime new group starts!!
			if k == ct_grouping[i]-1: # last ptIndex in the contour group
				ptIndexHelper.append(k+1)
			ptIndex = k + sum([ptIndexHelper[w+1] for w in range(i)])
			contourDict.setdefault(ContourIndex[i], []).append(ptAr[ptIndex])
		contourDict[ContourIndex[i]] = np.array(contourDict[ContourIndex[i]])
	
	fig = plt.figure()
	for n in ContourIndex:
		#fig.add_subplot(n+300).plot(contourDict[n][:, 0], -contourDict[n][:, 1], 'k')
		plt.plot(contourDict[n][:, 0], -contourDict[n][:, 1], 'k')
	
	plt.axis('off')
	fig.axes[-1].set_aspect('equal')
	
	if not plot_now:
		plt.close()

	return fig
	

def fig2np(fig):
	'''Converts fig-object to np-array as described here by Joe Kington:
	http://stackoverflow.com/questions/7821518/matplotlib-save-plot-to-numpy-array'''
	canvas = FigureCanvas(fig)
	fig.patch.set_alpha(0.0)
	ax = fig.add_subplot(111)
	ax.patch.set_alpha(0.0)
	 
	# If we haven't already shown or saved the plot, then we need to
	# draw the figure first...
	fig.tight_layout(pad=0)
	canvas.draw()

	# Get the RGBA buffer  the figure #http://blogs.candoerz.com/question/169767/pylab-use-plot-result-as-image-directly.aspx
	w,h = fig.canvas.get_width_height()
	buf = np.fromstring(canvas.tostring_argb(), dtype=np.uint8)
	buf.shape = (h, w, 4)
 
	# canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
	buf = np.roll(buf, 3, axis = 2)
	return buf

def pts2np(ct_grouping, pts_array):
	'''
	Converts the point array, which was extracted from an amira ascii spatial graph, to a numpy array
	'''
	dummy_figure = sg_plot(ct_grouping, pts_array)
	np_array = fig2np(dummy_figure)
	plt.close()
	
	return np_array


## Transformation (on a sptial graph)
def rotate(in_array, angle):
	'''
	function for rotation, applied to a spatial graph array
	'''
	data = in_array[:,[0,1]] 
	rot = np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
	
	return np.dot(data,rot)

def translate(in_array, x_d, y_d):
	'''
	function for tranlation, applied to a spatial graph array
	'''
	data = in_array[:,[0,1]] 
	translation = [x_d, y_d] 
	
	newdata = data + translation
	return newdata

## Cost functions and finidng offsets
def findMin(ct_grouping, ptArray, angle):
	rotated = rotate(ptArray, angle)
	xCordsR = rotated[:, 0]
	yCordsR = -rotated[:, 1]

	rotated_array = pts2np(ct_grouping, rotated)
	x_histo = np.sum(rotated_array[:,:,1], axis=0)
	x_minR = np.min(x_histo)
	
	plt.close()
	return x_minR


def findTurning(ct_grouping, ptArray, plot_fig = False):
	angle_range = np.arange(-np.pi/3, np.pi/3, 0.01)
							
	min_list = [findMin(ct_grouping, ptArray, i) for i in angle_range]
	
	plt.plot(angle_range, min_list)
	if not plot_fig:
		plt.close()
	
	min_index = np.argmin(min_list)
	
	return angle_range[min_index]

def midline_finder(ct_grouping, upright):
	fig_array = pts2np(ct_grouping, upright)
	x_hist = np.sum(fig_array[:,:,1], axis=0)
	x_hist_cut = [x_hist[i] for i in range(len(x_hist)) if x_hist[i] < 73440]
	min_index = np.argmin(x_hist_cut)
	binnum = 10000
	relative_dist = float(min_index) / float(len(x_hist_cut))
	xcord_upr = upright[:,0]
	x_space = np.linspace(min(xcord_upr), max(xcord_upr), binnum)
	midline = x_space[int(relative_dist*binnum)]
	
	return midline


def findoffset_x(ct_grouping1, ct_grouping2, upright1, upright2):
	midline1 = midline_finder(ct_grouping1, upright1)
	midline2 = midline_finder(ct_grouping2, upright2)
	offset = midline1 - midline2
	return offset

def y_cost(top_sorted1, bottom_sorted1, top_sorted2, bottom_sorted2):
	a = np.sum((top_sorted1[:,1]-top_sorted2[:,1])*(top_sorted1[:,1]-top_sorted2[:,1]))
	b = np.sum((bottom_sorted1[:,1]-bottom_sorted2[:,1])*(bottom_sorted1[:,1]-bottom_sorted2[:,1]))
	return a + b 


def findoffset_y(upright1, upright2, x_offset):
	
	upr_sorted = upright1[upright1[:,1].argsort()]

	top10perNum = int(len(upr_sorted)*0.1)
	bottom10perNum = -top10perNum
	top = upr_sorted[0:top10perNum]
	bottom = upr_sorted[bottom10perNum:-1]

	top_sorted1 = top[top[:,0].argsort()]
	bottom_sorted1 = bottom[bottom[:,0].argsort()]
	
	cost_list = []
	tr_list = range(-4000,4000)
	
	for i in tr_list:
		upright2_trs = translate(upright2, x_offset, i)
		upr2_sorted = upright2_trs[upright2_trs[:,1].argsort()]
		top10perNum2 = top10perNum
		bottom10perNum2 = -top10perNum

		top2 = upr2_sorted[0:top10perNum2]
		bottom2 = upr2_sorted[bottom10perNum2:-1]

		top_sorted2 = top2[top2[:,0].argsort()]
		bottom_sorted2 = bottom2[bottom2[:,0].argsort()]

		cost = y_cost(top_sorted1, bottom_sorted1, top_sorted2, bottom_sorted2)
		
		cost_list.append(cost)
			
	min_index = np.argmin(cost_list)
	
	return tr_list[min_index]


## Auto align function
def aligner(ct_g1, ct_g2, ptAr1, ptAr2):
	
	turning1 = findTurning(ct_g1, ptAr1)
	upright1 = rotate(ptAr1, turning1)
	turning2 = findTurning(ct_g2, ptAr2)
	upright2 = rotate(ptAr2, turning2)
	
	x_offset = findoffset_x(ct_g1, ct_g2, upright1, upright2)
	upright21 = translate(upright2, x_offset, 0) # upright2 gets updated 
	y_offset = findoffset_y(upright1, upright21, x_offset)
	upright2 = translate(upright21, 0, y_offset)
		
	return upright1, upright2

# def aligner_with_transmat(ct_g1, ct_g2, ptAr1, ptAr2):
	
# 	turning1 = findTurning(ct_g1, ptAr1)
# 	upright1 = rotate(ptAr1, turning1)
# 	turning2 = findTurning(ct_g2, ptAr2)
# 	upright2 = rotate(ptAr2, turning2)
	
# 	x_offset = findoffset_x(ct_g1, ct_g2, upright1, upright2)
# 	upright21 = translate(upright2, x_offset, 0) # upright2 gets updated 
# 	y_offset = findoffset_y(upright1, upright21, x_offset)
# 	upright2 = translate(upright21, 0, y_offset)
		
# 	return upright1, upright2, (turning1, turning2), (x_offset, y_offset)

def alignerDebug(ct_g1, ct_g2, ptAr1, ptAr2, plot_figure = False):
	
	turning1 = findTurning(ct_g1, ptAr1)
	upright1 = rotate(ptAr1, turning1)
	turning2 = findTurning(ct_g2, ptAr2)
	upright2 = rotate(ptAr2, turning2)
	
	x_offset = findoffset_x(ct_g1, ct_g2, upright1, upright2)
	upright21 = translate(upright2, x_offset, 0) # upright2 gets updated 
	y_offset = findoffset_y(upright1, upright21, x_offset)
	upright2 = translate(upright21, 0, y_offset)
	
	# plotting for visualization
	x_upr1 = upright1[:,0]
	y_upr1 = -upright1[:,1]
	x_upr2 = upright2[:,0]
	y_upr2 = -upright2[:,1]
	
	plt.figure (110)
	xs1 = ptAr1[:, 0]
	ys1 = -ptAr1[:, 1]
	xs2 = ptAr2[:, 0]
	ys2 = -ptAr2[:, 1]
	plt.title('Raw Spatial Graphs')
	plt.plot(xs1, ys1, color = 'b')
	plt.plot(xs2, ys2, color = 'r')
	
	if not plot_figure:
		plt.close()

	plt.figure(111)
	plt.title('Aligned Spatial Graphs')
	plt.plot(x_upr1, y_upr1, color = 'b')
	plt.plot(x_upr2, y_upr2, color = 'r')
	
	if not plot_figure:
		plt.close()
		
	return upright1, upright2

def upright(ct_g, ptAr):
	turning = findTurning(ct_g, ptAr)
	upright = rotate(ptAr, turning)
	return upright


# This function is assuming that the spatial graphs are ALREADY uprighted. 
# Finds the translation matrix that should be applied to ptAr2 to match ptAr1
def getAlignTranslation(ct_g1, ct_g2, ptAr1, ptAr2):
	# turning1 = findTurning(ct_g1, ptAr1)
	# upright1 = rotate(ptAr1, turning1)
	# turning2 = findTurning(ct_g2, ptAr2)
	# upright2 = rotate(ptAr2, turning2)
	
	x_offset = findoffset_x(ct_g1, ct_g2, ptAr1, ptAr2)
	ptAr2_2 = translate(ptAr2, x_offset, 0) # ptAr2 gets updated 
	y_offset = findoffset_y(ptAr1, ptAr2_2, x_offset)
	
	return x_offset,y_offset



############# Below is for a list of ptArs ####################
## NOTE: ptAr_list is a list of tuples (ct_gr, ptAr)
## Make sure to UPRIGHT all the slices first
## Matching the next slice to the current slice

## First Step: Upright all the slices
def getTurnings(ptAr_list, debug = False):
	angle_list = []
	index = 0 
	for ct_gr, ptAr in tqdm(ptAr_list):
		angle = findTurning(ct_gr, ptAr)
		angle_list.append(angle)

		if debug == True:
			print "Working on the ptAr index: #" + str(index)
			print "Uprighting Angle: " + str(angle * 180 / math.pi) + " degrees"
		index = index + 1

	return angle_list 


def getTurningsAndsave(ptAr_list, outputfile, debug = False):
	angle_list = []
	index = 0 
	print "Starting the calculation of turning angles... "
	for ct_gr, ptAr in tqdm(ptAr_list):
		# print "Working on the ptAr index: #" + str(index)
		angle = findTurning(ct_gr, ptAr)
		angle_list.append(angle)
		if debug == True:
			print "Working on the ptAr index: #" + str(index)
			print "Uprighting Angle: " + str(angle * 180 / math.pi) + " degrees"
		index = index + 1

		# open the file for writing
		fileObject = open(outputfile,'wb') 
		pickle.dump(angle_list, fileObject)  
		fileObject.close()

	# save file
	outputfile = outputfile + "_final"
	fileObject = open(outputfile,'wb') 
	pickle.dump(angle_list, fileObject)  
	fileObject.close()

	print "file saved and all done!"
	return angle_list 

def uprightAll(ptAr_list, angle_list):
	new_ptAr_list = []
	for k in range(len(ptAr_list)):
		new_ptAr = rotate(ptAr_list[k][1], angle_list[k])
		new_ptAr_list.append([ptAr_list[k][0], new_ptAr])

	return new_ptAr_list

## Second Step: Apply the tranlsations

# Doesn't change the input list -> need to manually apply the translations later 
def getAllTranslations(input_ptAr_list):
	ptAr_list = copy.deepcopy(input_ptAr_list)
	translation_list = []
	for i in range(len(ptAr_list)-1):
		ct_gr_current = ptAr_list[i][0]
		ptAr_current = ptAr_list[i][1]
		
		ct_gr_next = ptAr_list[i+1][0]
		ptAr_next = ptAr_list[i+1][1]
		
		x_offset, y_offset = getAlignTranslation(ct_gr_current, ct_gr_next, ptAr_current, ptAr_next)

		translation_list.append([x_offset, y_offset])
		ptAr_list[i+1][1] = translate(ptAr_list[i+1][1], x_offset, y_offset)

	return translation_list 

# Apply the translations 
def applyAndgetAllTranslations(ptAr_list):
	translation_list = []
	for i in range(len(ptAr_list)-1):
		ct_gr_current = ptAr_list[i][0]
		ptAr_current = ptAr_list[i][1]
		
		ct_gr_next = ptAr_list[i+1][0]
		ptAr_next = ptAr_list[i+1][1]
		
		x_offset, y_offset = getAlignTranslation(ct_gr_current, ct_gr_next, ptAr_current, ptAr_next)

		translation_list.append([x_offset, y_offset])
		ptAr_list[i+1][1] = translate(ptAr_list[i+1][1], x_offset, y_offset)

	return translation_list 

def applyAllTranslations(ptAr_list, translation_list):
	for i in range(len(translation_list)):
		x_offset = translation_list[i][0]
		y_offset = translation_list[i][1]
		ptAr_list[i+1][1] = translate(ptAr_list[i+1][1], x_offset, y_offset)
	
	return ptAr_list


def drawAll(ptAr_list):
	if len(ptAr_list) == 2:
		if len(ptAr_list[1]) == 2:
			plt.plot(ptAr_list[0][1][:,0], -ptAr_list[0][1][:,1])
			plt.plot(ptAr_list[1][1][:,0], -ptAr_list[1][1][:,1])
			
		else:
			plt.plot(ptAr_list[1][:,0], -ptAr_list[1][:,1])

	else:
		for each_ptAr_item in ptAr_list:
			#sg_plot(each_ptAr_item[0], each_ptAr_item[1], True)
			plt.plot(each_ptAr_item[1][:,0], -each_ptAr_item[1][:,1])