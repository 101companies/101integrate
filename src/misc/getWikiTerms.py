#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import simplejson as json

datafldr = ../../data/

if __name__ == "__main__":
  topics = ["concepts","themes","vocabularies","technologies","languages"]
  terms = dict()
  for t in topics:
    url = "http://worker.101companies.org/data/resources/"+t+"/members.json"
    print "Downloading:", url.rstrip()
    terms[t]= sorted(json.loads(urllib2.urlopen(url).read()))
  writer = open(datafldr+"terms.json","w")
  writer.write(json.dumps(terms, indent="\t"))
  writer.close()
  termlist = list()
  for k in terms.keys():
    for e in terms[k]:
      termlist.append([e,k])
  termlist.sort(key=lambda x: x[0].lower())
  writer = open(datafldr+"terms.csv","w")
  writer.write("Term;Type\r\n")
  for l in termlist:
    writer.write("\""+"\";\"".join(l)+"\"\r\n")
  writer.close()