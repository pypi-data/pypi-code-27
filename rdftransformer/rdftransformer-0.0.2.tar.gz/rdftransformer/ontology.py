# -*- coding: utf-8 -*-

import re
import os.path
import json
import rdflib
import ast
from evaluator import *

class Ontology:

	def __init__(self, ontologyLocation, prefix):
		self.ontologyLocation = ontologyLocation
		if self.__validateOntologyLocation():
			self.prefix = prefix
			self.ontology_raw = self.__importOntologyRaw()
			self.ontology = self.__importOntology()
			self.prefixes = self.__getPrefixes()
			self.classes = self.__getClasses(prefix)
			self.objectProperties = self.__getObjectProperties(prefix)
			self.dataProperties = self.__getDataProperties(prefix)
		else:
			print("File not Found!")

	def __validateOntologyLocation(self):
		return os.path.isfile(self.ontologyLocation)

	def __importOntologyRaw(self):
		fd = open(self.ontologyLocation, "r")
		read_data = []
		for line in fd:
			read_data.append(line)
		fd.close()
		return read_data

	def __importOntology(self):
		g=rdflib.Graph()
		g.load(self.ontologyLocation, format='turtle')
		j =  g.serialize(format = "json-ld")
		j = ast.literal_eval(j)
		return evaluateOntology(j)

	def __getPrefixes(self):
		prefixes = {}
		for line in self.ontology_raw:
			if '@prefix' in line:
				line = ''.join(line.split())
				prefix = line[7: line.find(":")]
				source = line[line.find("<")+1 : line.find(">")]
				prefixes[prefix] = source
		return prefixes

	def __getClasses(self, separator = "/"):
		classList = []
		for key in self.ontology.keys():
			className = key[key.rfind("/")+1:]
			if className:
				if "#Class" in self.ontology[key]["rdf:type"]:
					classList.append(className)
		return classList

	def __hasSubClasses(self, className):
		subClasses = []
		for nodeName in self.ontology:
			node = self.ontology[nodeName]
			if "http://www.w3.org/2002/07/owl#Class" in node["rdf:type"]:
				if "http://www.w3.org/2000/01/rdf-schema#subClassOf" in node.keys():
					superClasses = node["http://www.w3.org/2000/01/rdf-schema#subClassOf"]
					for superClass in superClasses:
						if isinstance(superClass, dict):
							if "http://www.w3.org/2002/07/owl#Class" in superClass["rdf:type"]:
								for names in superClass.values():
									if isinstance(names, list):
										for name in names:
											if className == name:
												subClasses.append(nodeName)
						if isinstance(superClass, str):
							if superClass == className:
								subClasses.append(nodeName)
		return subClasses

	def __getObjectProperties(self, separator = "/"):
		objectProperties = {}
		for key in self.ontology.keys():
			className = key[key.rfind("/")+1:]
			if className:
				if "#ObjectProperty" in self.ontology[key]["rdf:type"]:
					domainClasses = []
					for domain in self.ontology[key]["http://www.w3.org/2000/01/rdf-schema#domain"]:
						domainClasses.append(domain)
						for subClass in self.__hasSubClasses(domain):
							domainClasses.append(subClass)

					rangeClasses = []
					for rangeName in self.ontology[key]["http://www.w3.org/2000/01/rdf-schema#range"]:
						rangeClasses.append(rangeName)
						for subClass in self.__hasSubClasses(rangeName):
							rangeClasses.append(subClass)

					domainDict = {"domain" : domainClasses}
					rangeDict = {"range" : rangeClasses}
					objectProperties.update({className : domainDict})
					objectProperties[className].update(rangeDict)
		return objectProperties

	def __getDataProperties(self, separator = "/"):
		dataProperties = {}
		for key in self.ontology.keys():
			className = key[key.rfind("/")+1:]
			if className:
				if "#DatatypeProperty" in self.ontology[key]["rdf:type"]:
					domainClasses = []
					for domain in self.ontology[key]["http://www.w3.org/2000/01/rdf-schema#domain"]:
						domainClasses.append(domain)
						for subClass in self.__hasSubClasses(domain):
							domainClasses.append(subClass)

					rangeClasses = []
					for rangeName in self.ontology[key]["http://www.w3.org/2000/01/rdf-schema#range"]:
						rangeClasses.append(rangeName)
						for subClass in self.__hasSubClasses(rangeName):
							rangeClasses.append(subClass)

					domainDict = {"domain" : domainClasses}
					rangeDict = {"range" : rangeClasses}
					dataProperties.update({className : domainDict})
					dataProperties[className].update(rangeDict)
		return dataProperties

	# def __getClasses(self, prefix):
	# 	classes = []
	# 	for line in self.ontology:
	# 		line = ''.join(line.split())
	# 		if 'owl:Class;' in line:
	# 			className = line[len(prefix)+1:line.find("rdf:type")]
	# 			classes.append(className)
	# 	return classes

	# def __getDataProperties(self, prefix):
	# 	dataProperties = {}
	# 	propertyName = ""
	# 	domainClass = ""
	# 	rangeType = ""
	# 	isProperty = False
	# 	for line in self.ontology:
	# 		line = ''.join(line.split())
	# 		if isProperty:
	# 			if 'rdfs:domain' in line:
	# 				domainClass = line[line.find(prefix)+len(prefix) + 1:line.find(";")]
	# 			if "rdfs:range" in line:
	# 					rangeType = line[line.find("xsd:")+len("xsd:"):line.find(".")]
	# 			if line[-1:] == ".":
	# 				isProperty = False
	# 				dataProperties[propertyName] = {"domain" : domainClass, 'range' : rangeType}
	# 		else:
	# 			if 'owl:DatatypeProperty' in line:
	# 				isProperty = True
	# 				propertyName = line[len(prefix)+1:line.find("rdf:type")]
	# 	return dataProperties

	# def __getObjectProperties(self, prefix):
	# 	objectProperties = {}
	# 	propertyName = ""
	# 	domainClass = []
	# 	rangeClass = []
	# 	isProperty = False
	# 	isMultiLine = False
	# 	for line in self.ontology:
	# 		line = ''.join(line.split())
	# 		if isProperty:

				
	# 			if isMultiLine:
	# 				if ";" in line:
	# 					domainClass.append(line[line.find(prefix)+len(prefix) + 1:line.find(";")])
	# 				if "." in line:
	# 					rangeClass.append(line[line.find(prefix)+len(prefix) + 1:line.find(".")])
	# 				isMultiLine = False
	# 			else:
	# 				if 'rdfs:domain' in line:
	# 					if "," in line:
	# 						isMultiLine = True
	# 						domainClass.append(line[line.find(prefix)+len(prefix) + 1:line.find(",")])
	# 					else:
	# 						domainClass = line[line.find(prefix)+len(prefix) + 1:line.find(";")]

	# 				if "rdfs:range" in line:
	# 					if "," in line:
	# 						isMultiLine = True
	# 						rangeClass.append(line[line.find(prefix)+len(prefix) + 1:line.find(",")])
	# 					else:
	# 						rangeClass = line[line.find(prefix)+len(prefix) + 1:line.find(".")]
	# 			if line[-1:] == ".":
	# 				isProperty = False
	# 				objectProperties[propertyName] = {"domain" : domainClass, 'range' : rangeClass}
	# 				domainClass = []
	# 				rangeClass = []
	# 		else:
	# 			if 'owl:ObjectProperty' in line:
	# 				isProperty = True
	# 				propertyName = line[len(prefix)+1:line.find("rdf:type")]
	# 	return objectProperties

	def isClass(self, element):
		return element in self.classes

	def isObjectProperty(self, element):
		return element in self.objectProperties

	def isDataProperty(self, element):
		return element in self.dataProperties

	def isDefined(self, element):
		for dataProperty, value in self.dataProperties.items():
			for value in value["domain"]:
				if element in value:
					return True
		return False

	def printOntology(self, raw = False):
		if raw:
			for line in self.ontology_raw:
				print(line)
		else:
			print json.dumps(self.ontology, indent=2, sort_keys=True)



	# Function to use when expanding to ontology http import

	# def __validateOntologyLocation(self):
	# 	regex = re.compile(r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$', re.IGNORECASE)
	# 	if os.path.isfile(self.ontologyLocation) == True:
	# 		return False
	# 	elif (re.match(regex, self.ontologyLocation) is not None) == True:
	# 		return True
	# 	else:
	# 		return None