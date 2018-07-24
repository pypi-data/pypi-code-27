#-*- coding: utf-8 -*-
#!/usr/bin/env python


link = 'http://linkeddata.systems:3000'
base_link = 'https://purl.org/fair-metrics/'
from .showup import showin
import urllib2
import json


#def collectionS():
    #req = urllib2.urlopen(link+'/collections.json')
    #principle = raw_input("Choose your collections id or name: (Ex. 2, \"A Metrics\" or all)")
    #if "all" in principle:
        #showup(req)
    #else:
        #json_off = json.load(req)
        #for i in json_off:
            #if principle == str(i["id"]) or  str(principle).upper() == (i["name"]).upper():
                #for m in i:
                    #if type(i[m]) == list:
                        #showin(i[m])
                    #else:
                        #i[m] = str(i[m])
                        #print ("\t%s:  %s")%(m, i[m])
                #print "\n"
            #else:
                #continue


class Collections:

    def __init__(self, Id):
        sec = ("%s/collections/%s.json") % ( link, Id)
        self.req = urllib2.urlopen(sec)
        self.ID = json.load(self.req)


    def title(self):
        for i in self.ID:
            if self.ID[i] == self.ID["name"]:
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


    def _id(self):
        for i in self.ID:
            if self.ID[i] == self.ID["id"]:
                self.ID[i] = str(self.ID[i])
                return  self.ID[i]
                #print ("\t%s:  %s")%(i, self.ID[i])
        #print "\n"


    def organization(self):
          for i in self.ID:
            if self.ID[i] == self.ID["organization"]:
                self.ID[i] = str(self.ID[i])
                return  self.ID[i]
                #print ("\t%s:  %s")%(i, self.ID[i])
        #print "\n"


    def contact(self):
        for i in self.ID:
            if self.ID[i] == self.ID["contact"]:
                self.ID[i] = str(self.ID[i])
                return  self.ID[i]
                #print ("\t%s:  %s")%(i, self.ID[i])
        #print "\n"


    def metrics(self):
        for i in self.ID:
            if self.ID[i] == self.ID["metrics"]:
                x = showin(self.ID[i])
                return x
