#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import codecs
import json
import re
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

resourcename = sys.argv[1]
root = sys.argv[2]
resourcebase = root + sys.argv[1] + '/'
resInfos = json.loads(open("config/config.json", 'rb').read())
distribution = json.loads(open(resourcebase + sys.argv[3], 'rb').read())
termlinks = {}
lmtzr = WordNetLemmatizer()
posRegex = re.compile("(.*)\\$\\$\\$")
files = {}
filesn = {}
chapters = json.loads(open(resourcebase + "metadata/chapters.json", 'rb').read())['chapters']
for chapter in chapters:
	filen = chapter['file']
	filesn[filen] = chapter['title']
	parts = []
	for part in unicode(codecs.open(resourcebase + sys.argv[4] + filen, 'r', 'latin-1').read()).lower().split('$$$$'):
		poss = posRegex.findall(part)
		if poss:
			partid = '#' + poss[0].lstrip().rstrip()
		else:
			partid = ''
		stemmedPart = " " + " ".join(map(lambda t: lmtzr.lemmatize(t).lower(), nltk.wordpunct_tokenize(part))) + " "
		parts.append((partid, stemmedPart))
	files[filen]  = parts
for i, term in enumerate(distribution):
	primary = []
	print str(i) + "/" + str(len(distribution)) + " Backlinking " + term
	maxChaps = sorted(distribution[term], key=distribution[term].get, reverse=True)[:int(sys.argv[5])]
	for maxChap in maxChaps:
		maxFreq = distribution[term][maxChap]
		if maxFreq > 0:
			maxFileName = [c for c in distribution[term] if distribution[term][c] == maxFreq][0]
			if 'urlBase' in resInfos[resourcename]:
				maxLink = resInfos[resourcename]['urlBase'] + maxFileName.split('.')[0] + resInfos[resourcename]['ext']
			else:
				maxLink = resInfos[resourcename]['cite'].replace("$$$",filesn[maxFileName])
			for (partid, part) in files[maxFileName]:
				if " " + term.lower() + " " in part:
					maxLink += partid
					break
		else:
			maxLink = ''
		if maxLink:
			primary.append(maxLink)
	termlinks[term] = {'primary' : primary}
f = open(resourcebase + "backlinks.json", "write")
f.write(json.dumps(termlinks))
