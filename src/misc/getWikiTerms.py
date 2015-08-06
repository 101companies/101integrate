#!/usr/bin/env python
#coding=utf-8

import simplejson as json
import sys
import urllib2

def getTerms():
	result = []
	url = "http://data.101companies.org/resources/{}/members.json"
	mapping = {"concepts":"","languages":"Language:","technologies":"Technology:"}
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	for k in mapping.keys():
		infile = opener.open(url.format(k))
		data = sorted(json.load(infile), key=(lambda x: x.lower()) )
		for d in data:
			result.append(mapping[k]+d)
	return result

def writeTerms(outfile="../../data/allbooks/wikiTerms.csv"):
	terms = getTerms()
	writer = open(outfile, "w")
	for t in terms:
		writer.write(t)
		writer.write("\r\n")
	writer.close()

if __name__ == "__main__":
	writeTerms(*sys.argv[1:])

"""
http://data.101companies.org/resources/concepts/members.json
http://data.101companies.org/resources/languages/members.json
http://data.101companies.org/resources/technologies/members.json
"""
