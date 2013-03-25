import csv
import os
import sys
import re
import json
import csv
from collections import defaultdict
import inflect
p = inflect.engine()
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

def isinWhitelist(term, list):
	for t in list:
		if term.find(t) != -1:
			return True
	return False

def isAbb(term):
	for i in range(0, len(term)):
		if re.match("\/|\.|\-", term[i]):
			return True
	return False

def nonAbbtoLower(term):
	for i in range(0, len(term) - 1):
		if term[i].istitle() and term[i+1].istitle():
			return term
	for i in range(0, len(term)):
		if re.match("\/|\.|\-", term[i]):
			return term
	return term.lower()

resInfos = json.loads(open("config/config.json", 'rb').read())
# read index file
root = sys.argv[2]
resourcebase = root + sys.argv[3]
indexbase = root + sys.argv[4]
index = csv.reader(open(indexbase + sys.argv[5]), delimiter=',')
#input(index)
whitelist = []
whiteListReader = csv.reader(open("config/whitelist.csv", 'rb'), delimiter=',')
for row in whiteListReader:
	whitelist.append(row[0])
lmtzr = WordNetLemmatizer()

realcnamesraw = json.loads(open(resourcebase + sys.argv[6], 'rb').read())['chapters']
realcnames = {}
realcnamesl = []
for i,x in enumerate(realcnamesraw):
	realcnamesl.append(realcnamesraw[i]['file'])
	realcnames[realcnamesraw[i]['file']] = realcnamesraw[i]['title']

rawChapters = {}
stemmedChapters = {}
rawChaptersParts = {}
stemmedChaptersParts = {}
structure = []
listing = realcnamesl
posRegex = re.compile("(.*)\\$\\$\\$")
for l in listing:
	if not l.startswith(".") and l in realcnames:
		chapter = open(resourcebase + sys.argv[7] + l).read()
		rawChapters[l] = chapter
		print "Stemming chapter in", l
		stemmedChapter = " " + " ".join(map(lambda t: lmtzr.lemmatize(t).lower(), nltk.wordpunct_tokenize(chapter))) + " "
		stemmedChapters[l] = stemmedChapter
		stemmedChaptersParts[l] = {}
		cstructure = {'chapterid' : l}
		rawChaptersParts[l] = {}
		partids = []
 		for i, part in enumerate(chapter.split('$$$$')):
			poss = posRegex.findall(part)
			if poss:
				partid = poss[0].replace(' ','')
			else:
				partid = ''
			rawChaptersParts[l][partid] = part
			partids.append(partid)
		cstructure['partids'] = partids
		structure.append(cstructure)
 		for i, part in enumerate(stemmedChapter.split('$$$$')):
			stemmedChaptersParts[l][partids[i]] = part





terms = []
for row in index:
	exsplits = row[0].replace("\"", "").split("!")[0]
	terms.extend([exsplits.split(", ")[0]])

abbTerms = []
stemmedTerms = {}
orginals = {}

for term in terms:
	if isAbb(term) or isinWhitelist(term,whitelist):
		abbTerms.append(term)
		orginals[term] = term
	else:

		termtokens = map(lambda t: lmtzr.lemmatize(t).lower() , nltk.wordpunct_tokenize(term))
		stemmedTerm = " ".join(termtokens).replace(" - ", "-")
		print "Stemmed term:", term, "->", nltk.wordpunct_tokenize(term), "->", termtokens, "->", stemmedTerm
		stemmedTerms[term] = stemmedTerm
		orginals[stemmedTerm] = term

freqAll = {}
freqAllDistribution = {}
freqAllDistributionDeep = {}
for abbTerm in abbTerms:
	freq = 0
	freqDist = {}
	freqDistDeep = []
	for rawChaptero in structure:
		rawChapter = rawChaptero['chapterid']
		c = rawChapters[rawChapter].count(abbTerm)
		freq = freq + c
		freqDist[rawChapter] = c
		freqDistDeepC = []

		for partid in rawChaptero['partids']:
			freqDistDeepC.append(rawChaptersParts[rawChapter][partid].count(abbTerm))
		freqDistDeep.append(freqDistDeepC)
	freqAllDistributionDeep[abbTerm] = freqDistDeep
	freqAll[abbTerm] = freq
	freqAllDistribution[abbTerm] = freqDist

for stemmedTermName in stemmedTerms:
	stemmedTerm = stemmedTerms[stemmedTermName]
	freq = 0
	freqDist = {}
	freqDistDeep = []
	for stemmedChaptero in structure:
		stemmedChapter = stemmedChaptero['chapterid']
		c = stemmedChapters[stemmedChapter].count(" " + stemmedTerm + " ")
		freq = freq + c
		freqDist[stemmedChapter] = c
		freqDistDeepC = []
		for partid in stemmedChaptero['partids']:
			freqDistDeepC.append(stemmedChaptersParts[stemmedChapter][partid].count(stemmedTerm))
		freqDistDeep.append(freqDistDeepC)
	freqAllDistributionDeep[stemmedTerm] = freqDistDeep
	freqAll[stemmedTerm] = freq
	freqAllDistribution[stemmedTerm] = freqDist


if sys.argv[9] == "nonmerged":
	postfix = ""
elif sys.argv[9] == "merged":
	postfix = "Merged"

metainfo = json.loads(open(indexbase + sys.argv[8], 'rb').read())


w1 = csv.writer(open(resourcebase + "/frequencies"  + postfix + ".csv", 'wb'), delimiter=";")
w1.writerow(["Term", "Stemmed", "Variations", "Frequency"])

for (i,freq) in enumerate(freqAll):
	print "Writing " + str(i+1) + "/" + str(len(freqAll))
	w1.writerow([orginals[freq], freq, ", ".join(map(lambda x: str(x), metainfo[freq]["synonyms"])), freqAll[freq]])


w2 = csv.writer(open(resourcebase + "/frequenciesDistribution" + postfix + ".csv", 'wb'), delimiter=";")

cnames = rawChapters.keys()
used = []
for cname in cnames:
	if realcnames.has_key(cname):
		used.append(cname)


w2.writerow(["Term", "Stemmed", "Variations"] + map(lambda x: realcnames[x], realcnamesl))
for freq in freqAllDistribution:
	row = [orginals[freq], freq, ", ".join(map(lambda x: str(x), metainfo[freq]["synonyms"]))]
	for cname in realcnamesl:
		row.append(freqAllDistribution[freq][cname])
	w2.writerow(row)

f = open(resourcebase + "/frequencies" + postfix + ".json", 'write')
f.write(json.dumps(freqAll))

f = open(resourcebase + "/frequenciesDistribution" + postfix + ".json", 'write')
f.write(json.dumps(freqAllDistribution))

f = open(resourcebase + "/frequenciesDistributionDeep" + postfix + ".json", 'write')
f.write(json.dumps({'structure' : structure, 'distribution' : freqAllDistributionDeep}))
