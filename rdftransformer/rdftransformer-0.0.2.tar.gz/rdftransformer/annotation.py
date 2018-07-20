# -*- coding: utf-8 -*-

import re
import os.path
import json
import string, random
from helpers import isDate
from ontology import Ontology
from lxml import etree as ET
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib import RDF, RDFS, OWL, XSD


class Annotation:

	def __init__(self):
		self.graph = Graph()
		self.indent = 0
		self.depth = 0


	def importOntology(self, ontologyLocation, prefix = ""):
		self.ontology = Ontology(ontologyLocation, prefix)

		self.__addNamespaces()
		return self.ontology

	def importData(self, filename):
		if self.__validateDataLocation(filename):
			# self.namespaces = self.__getNamespaces(filename)
			self.data = ET.parse(filename)
			self.root = self.data.getroot()
			self.namespaces = self.root.nsmap
		else:
			print ("File not found!")
		return self.data

	def getElementsByTagName(self, tag, parent = "", namespaces = {}):
		tagPrefix = self.__getPrefixFromTag(tag)
		tagName =  self.__getNameFromTag(tag)

		parentPrefix = self.__getPrefixFromTag(parent)
		parentName = self.__getNameFromTag(parent)


		if not namespaces:
			if tagPrefix in self.namespaces:
				tagQuery =  "{" + self.namespaces[tagPrefix] + "}" + tagName
			else:
				tagQuery = tagName

			if parentPrefix in self.namespaces:
				parentQuery = "{" + self.namespaces[parentPrefix] + "}" + parentName
			else:
				parentQuery = parentName
		else:
			print (namespaces[tagPrefix])
			if tagPrefix in namespaces:
				tagQuery = "{" + namespaces[tagPrefix] + "}" + tagName
			else:
				tagQuery = tagName

			if parentPrefix in namespaces:
				parentQuery =  "{" + namespaces[parentPrefix] + "}" + parentName
			else:
				parentQuery = parentName

		query = ".//"

		if not parent:
			query = query + tagQuery
		else:
			query = query + parentQuery + "/" + tagQuery

		return self.root.findall(query)

		# TODO
		# def getElementByAttribute()



	def printRecur(self, root):
		"""Recursively prints the tree."""
		print (' '*self.indent + '%s: %s' % (root.tag, root.attrib.get('name', root.text)))
		self.indent += 4
		for elem in root.getchildren():
			self.printRecur(elem)
			self.indent -= 4

	def annotate(self, element, depth = 0, uid = ""):
		# print ("==========")
		# print ("%i:%s" % (depth, element.tag))
		tag = self.__getNameFromTag(element.tag, "}")
		

		if (self.ontology.isClass(tag)) and (depth == 0):
			# print "Class: " + tag
			uid = self.__getIdentifier(element)
			self.graph.add((self.ontologyNamespaces[self.ontology.prefix][uid], RDF.type, self.ontologyNamespaces[self.ontology.prefix][tag]))


		if self.ontology.isObjectProperty(tag):
			# print ("ObjectProperty: " + tag)
			# print (element.getparent().tag)
			children = element.getchildren()
			if len(children):
				o_domain = uid + "_" + tag
				o_range = self.__getNameFromTag(children[0].tag, "}")

				if self.ontology.isDefined(o_range):
					self.graph.add((self.ontologyNamespaces[self.ontology.prefix][uid], self.ontologyNamespaces[self.ontology.prefix][tag], self.ontologyNamespaces[self.ontology.prefix][o_domain]))
					self.graph.add((self.ontologyNamespaces[self.ontology.prefix][o_domain], RDF.type, self.ontologyNamespaces[self.ontology.prefix][o_range]))



		if self.ontology.isDataProperty(tag):
			# print ("DataProperty: " + tag)
			d_domain = self.ontology.dataProperties[tag]["domain"]
			# print (d_domain)
			# print (self.ontology.dataProperties[tag]["domain"][0])
			for domain in d_domain:
				for s,p,o in self.graph.triples( (None, None, URIRef(domain)) ):
					if uid in s:
						if isDate(element.text):
   							self.graph.add((s, self.ontologyNamespaces[self.ontology.prefix][tag], Literal(element.text, datatype=XSD.date)))
   						else:
   							self.graph.add((s, self.ontologyNamespaces[self.ontology.prefix][tag], Literal(element.text)))

   			
		# print ("==========")
		for elem in element.getchildren():
			depth += 1
			self.annotate(elem, depth, uid)
			depth -= 1

	def output(self, destination = None, format = "turtle"):
		if not destination:
			print self.graph.serialize(format = format)
		else:
			print "Output saved to " + destination
			self.graph.serialize(destination = destination, format = format)

	def __getPrefixFromTag(self, tag, separator = ":"):
		if separator in tag:
			prefix = tag[:tag.find(separator)]
			return prefix
		else:
			return None

	def __getNameFromTag(self, tag, separator = ":"):
		if separator in tag:
			name = tag[tag.find(separator) + 1 : ]
			return name
		else:
			return tag

	def __getIdentifier(self, element):
		for elem in element.getchildren():
			if self.namespaces["gml"] in elem.tag:
				return elem.text
			else:
				return self.__generateUniqueID(element)

	def __generateUniqueID(self, element):
		x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
		return "urn:adv:oid:" + x

	def __getNamespaces(self):
		namespaces = {}
		for name in self.ontology.prefixes:
			if (name == "owl") or (name == "xsd") or (name == "rdf") or (name == "rdfs"):
				continue
			else:
				namespaces[name] = Namespace(self.ontology.prefixes[name])
		self.ontologyNamespaces = namespaces
		return namespaces

	def __addNamespaces(self):
		for name_space, path in self.__getNamespaces().items():
			self.graph.bind(name_space, path)


	# TODO

	# OPTIONAL, We will see what is better
	# def __getNamespaces(self, filename):
	# 	fd = open(filename, "r")
	# 	read_data = {}
	# 	for line in fd:
	# 		if "xmlns" in line:
	# 			line = "".join(line.split())
	# 			if "xmlns=" in line:
	# 				read_data['default'] = line[line.find("=") + 2:-1]
	# 			if "xmlns:" in line:
	# 				read_data[line[line.find(":")+1:line.find("=")]] = line[line.find("=") + 2 : -1]
				
	# 	fd.close()
	# 	return read_data


	def __validateDataLocation(self, filename):
		return os.path.isfile(filename)