#-*- coding: utf-8 -*-
#!/usr/bin/env python


link = 'http://linkeddata.systems:3000'
base_link = 'https://purl.org/fair-metrics/'
import json


def showup(req):
    json_off = json.load(req)
    for i in json_off:
        for m in i:
            if type(i[m]) == list:
                showin(i[m])
            else:
                i[m] = str(i[m])
                print ("\t%s:  %s")%(m, i[m])
        print "\n"


def showin(ins):
    for i in ins:
        for m in i:
            if type(i[m]) == list:
                showin(ins[i])
            else:
                i[m] = str(i[m])
                print ("\t%s:  %s")%(m, i[m])
        print"\n"
