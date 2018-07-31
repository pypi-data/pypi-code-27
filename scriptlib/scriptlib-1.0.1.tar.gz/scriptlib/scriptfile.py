'''
ScriptFile
File Manager for the scriptlib package
Developed by Orbtial
'''

#Custom Imports
from . import scriptui

#Standard Imports
import os

def initPTPDIR(filePathAttr):
	"""
	Returns a string representation of the path to the file's parent directory.
	Should be initialised and stored before using any other function from the brickscript library that works with files.

	:param filePathAttr: Should be filled in with __file__ attribute from file calling this function.
	:return: String representing path to parent directory of file
	"""
	return os.path.dirname(os.path.realpath(filePathAttr))

def goToPath(ptpdir, path):
	"""
	Shifts current working directory to path specified relative to current working directory.

	:param ptpdir: String generated from initPTPDIR().
	:param path: String representing path to move to relative to current working directory.
	"""
	os.chdir(ptpdir+"/{}".format(path))

def wFileData(ptpdir, path, filename, data, isOverwrite):
	"""
	Appends or overwrites text to file specified.

	:param ptpdir: String generated from initPTPDIR().
	:param path: String representing path to file starting from parent directory of file.
	:param filename: String representing name of file to be written or appended to and should include filetype extension.
	:param data: String representing text of which should be written or appended to said file.
	:param isOverwrite: Boolean indicating whether the file should be overwritten instead of being appended by default.
	"""
	goToPath(ptpdir, path)
	mode = "a"
	if isOverwrite: mode = "w"
	with open(filename, mode) as f:
		f.write(data)

def rFileData(ptpdir, path, filename):
	"""
	Returns text from file specified as a raw string.

	:param ptpdir: String generated from initPTPDIR().
	:param path: String representing path to file starting from parent directory of file.
	:param filename: String representing name of file to be written or appended to and should include filetype extension.
	:return: String representing text contained inside file.
	"""
	goToPath(ptpdir, path)
	with open(filename, "r") as f:
		data = "".join(f.readlines())
		return data

def gInternalFile(ptpdir, path, question):
	"""
	UI element that allows a user to choose a file from a directory, provided the file is not prepended with a "." character.

	:param ptpdir: String generated from initPTPDIR().
	:param path: String representing path to directory starting from parent directory of file.
	:param question: String representing prompt to be displayed to user.
	:return: String representing name of file chosen by user.
	"""
	goToPath(ptpdir, path)
	items = os.listdir()
	filename = scriptui.gList(question, [x for x in items if x[0] != "."], False)
	print(filename)
	return filename

def mFile(ptpdir, path, data, filename, fileType):
	"""
	UI element that allows the user to generate a file with data provided a filename and type extension.

	:param ptpdir: String generated from initPTPDIR().
	:param path: String representing path to directory containing new file, starting from parent directory of file.
	:param data: String representing initial text of file created.
	:param filename: String representing name of file to be created.
	:param fileType: String representing type extension of file to be created.
	"""
	goToPath(ptpdir, path)
	while True:
		scriptui.refresh()
		filename = input("Name of new file: ")
		if os.path.exists(filename+fileType):
			scriptui.errorMessage("That file already exists!")
		else:
			break
	wFileData(ptpdir, path, filename+fileType, data, True)
