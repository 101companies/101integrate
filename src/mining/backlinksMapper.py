#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import simplejson as json
import csv
import re
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

resourcename = sys.argv[1]
root = sys.argv[2]
resourcebase = root + sys.argv[1] + '/'
resInfos = json.loads(open("config/config.json", 'rb').read())
distributionraw = json.loads(open(resourcebase + sys.argv[3], 'rb').read())
distribution = distributionraw['distribution']
termlinks = {}
structure = distributionraw['structure']
hasUrl = 'urlBase' in resInfos[resourcename]
filesn = {}
print "Backlinking", resourcename, "..."
profileReader = csv.reader(open(resourcebase + 'chapterProfile.numbers.csv'), delimiter=',')
profile = {}
for row in profileReader:
	profile[row[1]] = row[2:]
chapters = json.loads(open(resourcebase + "metadata/chapters.json", 'rb').read())['chapters']
for chapter in chapters:
	filen = chapter['file']
	filesn[filen] = chapter['title']
for i, term in enumerate(distribution):
	if term == "monad":
		print "Yes"
	shallow = map(lambda x : sum(x), distribution[term])
	maxChapIndecies = [i[0] for i in sorted(enumerate(shallow), reverse=True, key=lambda x:x[1])][:int(sys.argv[5])]
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
				maxLinkID = resInfos[resourcename]['urlBase'] + maxFileName.split('.')[0] + resInfos[resourcename]['ext']
				maxLinkID += "#" + structure[maxChapIndex]['partids'][firstOcc]
			else:
				maxLinkID = resInfos[resourcename]['cite'].replace("$$$",filesn[maxFileName])
			maxLink = {'full': maxLinkID, 'chapter': filesn[maxFileName]}
			if isPrime:
				primary.append(maxLink)
			else:
				secondary.append(maxLink)
	termlinks[term] = {'primary' : primary, 'secondary' : secondary}
	if term == "monad":
		for s in secondary:
			print s
f = open(resourcebase + "backlinks.json", "write")
f.write(json.dumps(termlinks), indent= "\t")


