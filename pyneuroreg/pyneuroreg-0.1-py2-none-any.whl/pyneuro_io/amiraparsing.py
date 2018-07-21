import pyparsing as pp
import numpy as np
'''
Generalized Parser for amira ascii files using pyparsing 

Works with: amira spatial graphs or amira landmarks or amira-ascii-transformed morphology files

written by Peter Park 
'''

versionNum = 0.53 # June.20.2018

## BNF Grammar for amiraParsing 
pp.ParserElement.setDefaultWhitespaceChars(' \t')

at = '@'
EOL = pp.LineEnd().suppress()
code = pp.Combine(at+pp.Word(pp.nums,exact=1)) + EOL
point = pp.Literal(".")
comma = pp.Literal(",")
e = pp.CaselessLiteral("e")

fnumber = pp.Combine (pp.Word( "+-" + pp.nums, pp.nums ) + pp.Optional( point + pp.Optional( pp.Word(pp.nums))) + 
		pp.Optional(e + pp.Word("+-" +pp.nums, pp.nums)))

fnumber2 = pp.Word(pp.nums + '.')

fnumbers = pp.Group(pp.ZeroOrMore(fnumber) + EOL) + pp.ZeroOrMore(EOL)
valueList = pp.ZeroOrMore(fnumbers)

params = pp.Keyword("Parameters")
TFmatKey = pp.Keyword("TransformationMatrix")
dataSec = pp.Keyword('# Data section follows') + EOL

beforeEdgePoints = pp.Keyword("@6") + EOL
afterEdgePoints = pp.Keyword("@7") + EOL

## for surfaces 
vertices = pp.Keyword("Vertices") 
verticenum = pp.Keyword("Vertices").suppress() + fnumbers
triangles = pp.Keyword("Triangles") 
trianglesnum = pp.Keyword("Triangles").suppress() + fnumbers 



### Parameter Categorization (originally for morphology registration)

# 
Id = pp.Keyword('Id') + pp.Word(pp.nums)
Color = pp.Keyword('Color') + pp.Group(fnumber2 + fnumber2 + fnumber2)
open_bracket = pp.Literal('{')
close_bracket = pp.Literal('}')

# Level 0 Group
# just skip before GraphLabels
GraphLabels = pp.Keyword('GraphLabels')

# Level 1 Group
Neuron = pp.Keyword('Neuron')
Landmark = pp.Keyword('Landmark')

# Level 2 Group 
Dendrite = pp.Keyword('Dendrite')
Axon = pp.Keyword('Axon')
Soma = pp.Keyword('Soma')

Pia = pp.Keyword('Pia')
Vessel = pp.Keyword('Vessel')
Barrel = pp.Keyword('Barrel')

# Level 3 Group
ApicalDendrite = pp.Keyword('ApicalDendrite')
BasalDendrite = pp.Keyword('BasalDendrite')
Row_index_small = 'abcde'
greek = pp.Keyword('greek')
Row = pp.Keyword('Row')

Row_name = pp.Or(Row_index_small, greek)
Row_group = pp.Combine(Row_name, Row) + pp.WordEnd()

# Lveel 4 Group
Row_index_big = 'ABCDE'
Row_code = pp.Combine(pp.Word(Row_index_big, exact=1) + pp.Word(pp.nums,exact=1)) + pp.WordEnd()

Alpha = 'Alpha'
Beta = 'Beta'
Gamma = 'Gamma'
Delta = 'Delta'

###

param_list = ['ApicalDendrite', 'BasalDendrite', 'Axon', 'Soma', 'Pia', 'WM',
              'A1','A2','A3','A4',
              'B1','B2','B3','B4',
              'C1','C2','C3','C4','C5','C6',
              'D1','D2','D3','D4','D5','D6',
              'E1','E2','E3','E4','E5','E6',
              'Alpha','Beta','Gamma','Delta']


###########################
## Parsing Function 
def amiraParsing (file):
	inFile = open(file)
	text = inFile.read()

	skipBlock = pp.SkipTo(dataSec).suppress() # Parts that we skip parsing
	codeDict = pp.dictOf(code, valueList)
	whole = skipBlock + dataSec.suppress() + codeDict
	wholeParse = whole.parseString(text)
	return wholeParse

# Parsing Function with indexing: returns ParseResults object
def amiraParsingIndex(file, index):
	inFile = open(file)
	text = inFile.read()

	skipBlock = pp.SkipTo(dataSec).suppress() # Parts that we skip parsing
	codeDict = pp.dictOf(code, valueList)
	whole = skipBlock + dataSec.suppress() + codeDict
	wholeParse = whole.parseString(text)
	return wholeParse['@'+str(index)]

# Parsing multiple indices all at once
def amiraParsingIndex_multiple(file, index_list):
	inFile = open(file)
	text = inFile.read()

	skipBlock = pp.SkipTo(dataSec).suppress() # Parts that we skip parsing
	codeDict = pp.dictOf(code, valueList)
	whole = skipBlock + dataSec.suppress() + codeDict
	wholeParse = whole.parseString(text)

	ParsedList = []

	for index in index_list:
		ParsedList.append(wholeParse['@'+str(index)])

	return ParsedList


def amiraParsingBeforeEdgePoints(file):
	inFile = open(file)
	text = inFile.read()
	beforeBlock = pp.SkipTo(beforeEdgePoints)
	thisParse = beforeBlock.parseString(text)
	thisParseStr = thisParse[0]
	return thisParse

# Displays the header: returns ParseResults object
def amiraParsingHeader(file):
	inFile = open(file)
	text = inFile.read()
	headerBlock = pp.SkipTo(dataSec)
	thisParse = headerBlock.parseString(text)
	thisParseStr = thisParse[0]
	return thisParseStr

def amiraParsingHeaderAfterDefine(file):
	inFile = open(file)
	text = inFile.read()
	skipBlock = pp.SkipTo(params)
	headerBlock = pp.SkipTo(dataSec)
	this = skipBlock.suppress() + headerBlock
	thisParse = this.parseString(text)
	thisParseStr = thisParse[0]
	return thisParseStr

# Displays the parameters: : returns ParseResults object
def amiraParsingParameters(file):
	inFile = open(file)
	text = inFile.read()
	skipBlock1 = pp.SkipTo(params).suppress()
	skipBlock2 = pp.SkipTo(dataSec)
	skipBlockSum = skipBlock1 + skipBlock2
	thisParse = skipBlockSum.parseString(text)
	thisParseStr = thisParse[0]
	return thisParseStr

def amiraParsingLandmarks(file):
	inFile = open(file)
	text = inFile.read()
	skipBlock = pp.SkipTo(dataSec).suppress()
	this = skipBlock + dataSec.suppress() + code.suppress() + valueList
	thisParse = this.parseString(text)

	return thisParse


def amiraParsingSurface(file):
	inFile = open(file)
	text = inFile.read()

	skipBlock1 = pp.SkipTo(vertices).suppress()
	firstpart = pp.Group(skipBlock1 + verticenum.suppress() + valueList)
	skipBlock2 = pp.SkipTo(triangles).suppress()
	secondpart = skipBlock2 + trianglesnum.suppress() + pp.Group(valueList)
	whole = firstpart + secondpart
	wholeParse = whole.parseString(text)
	return wholeParse

# Parse the rest of file after the vertex 
# Used for surfacewriter.py
def amiraParsingSurfaceExceptVertex(file): 
	inFile = open(file)
	text = inFile.read()

	skipBlock1 = pp.SkipTo(vertices)
	firstpart = skipBlock1 + verticenum.suppress() + valueList.suppress()
	Tris_info_Block = pp.SkipTo(triangles)
	Tris_vals = pp.SkipTo('}', include = True)
	#secondpart = skipBlock2 + trianglesnum + valueList
	secondpart = Tris_info_Block + Tris_vals
	whole = firstpart + secondpart
	wholeParse = whole.parseString(text)
	return wholeParse


def amiraParsingSurfaceInfo(file):
	inFile = open(file)
	text = inFile.read()

	skipBlock1 = pp.SkipTo(vertices).suppress()
	firstpart = skipBlock1 + verticenum + valueList.suppress()
	skipBlock2 = pp.SkipTo(triangles).suppress()
	secondpart = skipBlock2 + trianglesnum + valueList.suppress()
	whole = firstpart + secondpart
	wholeParse = whole.parseString(text)
	return wholeParse

def amiraParsingSurfaceTriangles(file):
	inFile = open(file)
	text = inFile.read()

	skipBlock2 = pp.SkipTo(triangles).suppress()
	secondpart = skipBlock2 + trianglesnum.suppress() + valueList
	wholeParse = secondpart.parseString(text)
	return wholeParse

# Returns the transformation data: : returns ParseResults object
def amiraParsingTransformation(file):
	inFile = open(file)
	text = inFile.read()
	TFmat = TFmatKey + fnumbers + pp.Keyword("}")
	skipBlock1 = pp.SkipTo(TFmatKey).suppress() 
	TFParse = pp.Optional(skipBlock1 + TFmat)
	try:
		thisParse = TFParse.parseString(text)
		thisParseStr = thisParse[1]
		return thisParseStr

	except IndexError:
		print("Error: TransformationMatrix does not exist")

	else:
		print("Error: Check the ascii file again. The grammar rule cannot be applied to the file")

##### HOC-> Ascii READER 

def amiraParsingMorphHelper(input_str, i_type):
	skipBlock1 = pp.SkipTo(i_type)

	type_word = pp.Keyword(i_type)
	Vals = type_word + open_bracket.suppress() + EOL + Color + comma.suppress() + EOL + Id + EOL + close_bracket.suppress()

	whole = skipBlock1.suppress() + Vals

	# ColorCode = wholeParse[2]
	# IdCode = wholeParse[4]

	# wholeParse = whole.parseString(input_str)
	# return wholeParse

	try: 
		wholeParse = whole.parseString(input_str)
		return wholeParse

	except Exception:
		print ("Error: The input type may not be at the lowest level of categories.")


def amiraParsingMorph_getID(input_str, i_type):
	skipBlock1 = pp.SkipTo(i_type)

	type_word = pp.Keyword(i_type)
	Vals = type_word + open_bracket.suppress() + EOL + Color + comma.suppress() + EOL + Id + EOL + close_bracket.suppress()

	whole = skipBlock1.suppress() + Vals

	try: 
	# ColorCode = wholeParse[2]
	# IdCode = wholeParse[4]

		wholeParse = whole.parseString(input_str)
		return int(wholeParse[4])

	except Exception:
		print ("Error: The input type may not be at the lowest level of categories.")


def amiraParsingMorph(input_file, i_type, print_types = False, print_type_key= False):
	parsed_list = amiraParsingIndex_multiple(input_file, [4,5,6])

	NumEdgePts = convertToInt2(parsed_list[0])
	GraphLabels = convertToInt2(parsed_list[1])
	ptAr = convertToNParray(parsed_list[2])

	param_parsed = amiraParsingParameters(input_file)

	assorted_collection = {}

	param_dict = {}

	for param in param_list:
	    Id = amiraParsingMorph_getID(param_parsed, param)
	    param_dict[Id] = param

	if print_types == True: 
		print "----Parameter List----"
		print param_dict.values()

	if print_type_key == True: 
		print "----Parameter List KEY:VALUE----"
		print param_dict 
		# return param_dict

	for i in range(len(GraphLabels)):
	    last_index = sum(NumEdgePts[:i])
	    # print GraphLabels
	    Id = GraphLabels[i]
	    # print Id
	    ptAr_inRange = ptAr[last_index:last_index + NumEdgePts[i]]
	    # print ptAr_inRange
	    assorted_collection.setdefault(param_dict[Id],[]).append(ptAr_inRange)

	try: 
		npArray_parsed = np.vstack(assorted_collection[i_type])
		return npArray_parsed

	except Exception:
		print ("Error: The input type may not exist or be at the lowest level of categories.")


######


# Converts the ParseResult object to list of strings 
def convertToList(parseResult):
	return [list(parseResult[i]) for i in range(len(parseResult))]

# Converts the ParseResult object to list of floats 
def convertToFloat(parseResult):
	return [map(float, list(parseResult[i])) for i in range(len(parseResult))]

def convertToInt(parseResult):
	return [map(int, list(parseResult[i])) for i in range(len(parseResult))]

# Each element is not a list, but int. 
def convertToInt2(parseResult):
	return [int(list(parseResult[i])[0]) for i in range(len(parseResult))]

def convertToNParray(parseResult):
	return np.asarray(convertToFloat(parseResult)) 





# ## DEBUG
# input = '/Users/peterpark/Documents/Amira_contours_ascii/S062_BF_ct.am'
# directory = '/Users/peterpark/Library/Mobile Documents/com~apple~CloudDocs/Work/Image_processing_scripts/Tangential/TangentialData/'
# file1 = 'LandmarksWithin_output_dec14_simplified.landmarkAscii'

# input1 = directory + file1
# ga = amiraParsingLandmarks(input1)
# print ga
# print "amiraParsing Version: " + str(versionNum)
# file1 = 'Barrels.surf'
# input1 = directory + file1 

# test = amiraParsingSurface2(input1)
# print test[0]

# print len(test[0])
# print 'DONE'

# testinput = '/Users/peterpark/Documents/test_eg.txt'
# a = amiraParsing(input)
# print a
# print a[0]
# # #print (a['@3'])


# b = amiraParsingHeader(input)
# print(b)

# # c = amiraParsingTransformation(input)
# # #print(c)

# d = amiraParsingParameters(input)
# print d
# e = beforeEdgePoints(input)
# print e

# f = amiraParsingHeaderAfterDefine(input)
# print f
#print(d)
#print (b)

