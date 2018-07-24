#-*- coding: utf-8 -*-
#!/usr/bin/env python


link = 'http://linkeddata.systems:3000'
base_link = 'https://purl.org/fair-metrics/'
import urllib2
import json


#def metrics():
    #req = urllib2.urlopen(link+'/metrics.json')
    #principle = raw_input("Choose your principle: (Ex. R1.1, I3 or all)")
    #if "all" in principle:
        #showup(req)
    #else:
        #json_off = json.load(req)
        #for i in json_off:
            #if base_link+principle.upper() == (i["principle"]).upper():
                #for m in i:
                    #if type(i[m]) == list:
                        #showin(i[m])
                    #else:
                        #i[m] = str(i[m])
                        #print ("\t%s:  %s")%(m, i[m])
                #print "\n"
            #else:
                #continue


class Metrics:

    def __init__(self, Id):
        sec = ("%s/metrics/%s.json") % ( link, Id)
        self.req = urllib2.urlopen(sec)
        self.ID = json.load(self.req)


    def title(self):
        for i in self.ID:
            if self.ID[i] == self.ID["name"]:
                self.ID[i] = str(self.ID[i])
                return  self.ID[i]
                #print ("\t%s:  %s")%(i, self.ID[i])
        #print "\n"


    def smarturl(self):
        for i in self.ID:
            if self.ID[i] == self.ID["smarturl"]:
                self.ID[i] = str(self.ID[i])
                return  self.ID[i]
                #print ("\t%s:  %s")%(i, self.ID[i])
        #print "\n"


    def creator(self):
        for i in self.ID:
            if self.ID[i] == self.ID["creator"]:
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


    def principle(self):
          for i in self.ID:
            if self.ID[i] == self.ID["principle"]:
                self.ID[i] = str(self.ID[i])
                return  self.ID[i]
                #print ("\t%s:  %s")%(i, self.ID[i])
        #print "\n"


    def contact(self):
        for i in self.ID:
            if self.ID[i] == self.ID["email"]:
                self.ID[i] = str(self.ID[i])
                return  self.ID[i]
                #print ("\t%s:  %s")%(i, self.ID[i])
        #print "\n"
