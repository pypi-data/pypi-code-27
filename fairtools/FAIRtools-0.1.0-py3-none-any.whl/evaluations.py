#-*- coding: utf-8 -*-
#!/usr/bin/env python


link = 'http://linkeddata.systems:3000'
base_link = 'https://purl.org/fair-metrics/'
import urllib2
import json


#def evaluations():
    #req = urllib2.urlopen(link+'/evaluations.json')
    #principle = raw_input("Choose your evaluations id : (Ex. 2, 4 or all)")
    #if "all" in principle:
        #showup(req)
    #else:
        #json_off = json.load(req)
        #for i in json_off:
            #if principle == str(i["id"]):
                #for m in i:
                    #if type(i[m]) == list:
                        #showin(i[m])
                    #else:
                        #i[m] = str(i[m])
                        #print ("\t%s:  %s")%(m, i[m])
                #print "\n"
            #else:
                #continue


class Evaluations:

    def __init__(self, Id):
        sec = ("%s/evaluations/%s.json") % ( link, Id)
        self.req = urllib2.urlopen(sec)
        self.ID = json.load(self.req)


    def title(self):
        for i in self.ID:
            if self.ID[i] == self.ID["title"]:
                self.ID[i] = str(self.ID[i])
                return  self.ID[i]
                #print ("\t%s:  %s")%(i, self.ID[i])
        #print "\n"


    def url(self):
        for i in self.ID:
            if self.ID[i] == self.ID["url"]:
                self.ID[i] = str(self.ID[i])
                return  self.ID[i]
                #print ("\t%s:  %s")%(i, self.ID[i])
        #print "\n"


    def resource(self):
        for i in self.ID:
            if self.ID[i] == self.ID["resource"]:
                self.ID[i] = str(self.ID[i])
                return  self.ID[i]
                #print ("\t%s:  %s")%(i, self.ID[i])
                #print "\n"


    def _id(self):
        for i in self.ID:
            if self.ID[i] == self.ID["id"]:
                self.ID[i] = str(self.ID[i])
                return  self.ID[i]
                #print ("\t%s:  %s")%(i, self.ID[i])
        #print "\n"


    def body(self):
          for i in self.ID:
            if self.ID[i] == self.ID["body"]:
                self.ID[i] = str(self.ID[i])
                return  self.ID[i]
                #print ("\t%s:  %s")%(i, self.ID[i])
        #print "\n"


    def executor(self):
        for i in self.ID:
            if self.ID[i] == self.ID["executor"]:
                self.ID[i] = str(self.ID[i])
                return  self.ID[i]
                #print ("\t%s:  %s")%(i, self.ID[i])
        #print "\n"


    def collection(self):
        for i in self.ID:
            if self.ID[i] == self.ID["collection"]:
                self.ID[i] = str(self.ID[i])
                return  self.ID[i]
                #print ("\t%s:  %s")%(i, self.ID[i])
        #print "\n"x
