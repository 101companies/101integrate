#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import simplejson as json
import csv
import re
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import logging
import logging.config

## retrieves term location in book for backlinking
# @param	resourcename		the resource's folder name
# @param	root			the book data root folder (perbook-folder)
# @param	distributionfile	a json-file containing the frequencies of terms per book section 
# @param	limit			which n chapters with higest term frequency to use
def main(resourcename, root, distributionfile, limit):
  resourcebase = root + resourcename + '/'
  resInfos = json.loads(open("../config/config.json", 'rb').read())
  distributionraw = json.loads(open(resourcebase + distributionfile, 'rb').read())
  distribution = distributionraw['distribution']
  termlinks = {}
  structure = distributionraw['structure']
  hasUrl = 'urlBase' in resInfos[resourcename]
  filesn = {}
  logging.info("Backlinking" +  resourcename + "...")
  profileReader = csv.reader(open(resourcebase + 'chapterProfile.numbers.csv'), delimiter=',')
  profile = {}
  for row in profileReader:
	profile[row[1]] = row[2:]
  chapters = json.loads(open(resourcebase + "metadata/chapters.json", 'rb').read())['chapters']
  for chapter in chapters:
	filen = chapter['file']
	filesn[filen] = chapter['title']
  for i, term in enumerate(distribution):
	shallow = map(lambda x : sum(x), distribution[term])#Term occurence in whole chapters
	maxChapIndecies = [i[0] for i in sorted(enumerate(shallow), reverse=True, key=lambda x:x[1])][:int(limit)]
	primary = []
	secondary = []
	for maxChapIndex in maxChapIndecies:
		isPrime = False
		if term in profile and profile[term][maxChapIndex] != " ":
			isPrime = True
		parapraphDistribution = distribution[term][maxChapIndex]
		if sum(parapraphDistribution) > 0:
			maxFileName = structure[maxChapIndex]['chapterid']
			parapraphDistribution = distribution[term][maxChapIndex]
			firstOcc = parapraphDistribution.index(filter(lambda x : x > 0, parapraphDistribution)[0])
			if hasUrl:
				urlBase = resInfos[resourcename]['urlBase']
				if not urlBase.endswith("/"):
				    urlBase +="/"
				ext = resInfos[resourcename]['ext']
				if ext:
				    maxLinkID = urlBase + "/".join(maxFileName.split('.')[:-2])+ext
				else:
				    maxLinkID = urlBase + "/".join(maxFileName.split('.')[:-1])
				maxLinkID += "#" + structure[maxChapIndex]['partids'][firstOcc]
			else:
				maxLinkID = resInfos[resourcename]['cite'].replace("$$$",filesn[maxFileName])
			maxLink = {'full': maxLinkID, 'chapter': filesn[maxFileName]}
			if isPrime:
				primary.append(maxLink)
			else:
				secondary.append(maxLink)
	termlinks[term] = {'primary' : primary, 'secondary' : secondary}
  f = open(resourcebase + "backlinks.json", "write")
  f.write(json.dumps(termlinks, indent= "\t"))

if __name__ == "__main__":
	logging.config.fileConfig('../config/pythonLogging.conf')
	main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
