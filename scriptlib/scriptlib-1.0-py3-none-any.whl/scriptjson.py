'''
ScriptJSON
Json Manager for the scriptlib package
Developed by Orbtial
'''

#Custom Imports
from . import scriptfile

#Standard Imports
import json

def loadJson(ptpdir, path, filename):
	"""
	Returns a dictionary based on data from the specified .json file 

	:param ptpdir: String generated from initPTPDIR().
	:param path: String representing path of .json file relative to current working directory.
	:param filename: String representing name of .json file.
	:returns: Dictionary representing data from specified file.
	"""
	return json.loads(brickfile.rFileData(ptpdir, path, filename))

def writeJson(ptpdir, path, filename, dictionary):
	"""
	Overwrites a .json file with a JSON-formatted dictionary.
	
	:param ptpdir: String generated from initPTPDIR().
	:param path: String representing path of .json file relative to current working directory.
	:param filename: String representing name of .json file.
	:param dictionary: Dictionary containing data of which to be written to the file in JSON format.
	"""
	brickfile.wFileData(ptpdir, path, filename, json.dumps(dictionary), True)
