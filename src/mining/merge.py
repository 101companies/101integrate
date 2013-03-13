'''
 Merges all given index files by removing synonyms,
 creates a metadata file holding synonyms and resource names
'''
import csv
import sys
import inflect
import json
import re
import patternCleaner
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
			print ">>>>>", term
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

# we apply some very basic heuristics
def areSimilar(term1, term2):
	lmtzr = WordNetLemmatizer()
	return lmtzr.lemmatize(term1.lower()) == lmtzr.lemmatize(term2.lower())

# merge term indecies
allTerms = {}
resInfos = json.loads(open("config/config.json", 'rb').read())
commonEnglishWords = map(lambda x: x[0], list(csv.reader(open("../../data/allbooks/cache/rank.csv", 'rU'), delimiter=','))[:int(sys.argv[-2])])

changedByPattern = []

blacklist = json.loads(open("config/blacklist.json", 'rb').read())['blacklist']
whitelist = []
whiteListReader = csv.reader(open("config/whitelist.csv", 'rb'), delimiter=',')
for row in whiteListReader:
	whitelist.append(row[0])
#input(sys.argv[3:-5])
for csvfn in sys.argv[3:-5]:
	resourcename = sys.argv[1] + sys.argv[2]+ csvfn + "/" + sys.argv[-5]

	indexReader = csv.reader(open(resourcename, 'rb'), delimiter=',')
	print "Reading", resourcename
	preTerms = []
	for row in indexReader:
		exsplit = row[0].replace("\"", "").split("!")[0]
		preTerms.extend([exsplit.split(", ")[0]])
	for termUW in preTerms:
		termU = termUW.lstrip().rstrip()
		if not termU in blacklist and not termU in commonEnglishWords:
			if isinWhitelist(termU,whitelist):
				term = termU
			else:
				term = patternCleaner.cleanPatterns(nonAbbtoLower(termU), resInfos[csvfn]['exclude-patterns'])
				if term != nonAbbtoLower(termU):
					changedByPattern.append([nonAbbtoLower(termU),term])
			if allTerms.has_key(term):
				allTerms[term.lstrip(' ')]['resourcenames'].add(csvfn)
			else:
				allTerms[term.lstrip(' ')] = dict(resourcenames = set([csvfn]))
		else:
			print "Blacklisted term", termU, "excluded"

# detect synonyms
synonyms = []
for i, term in enumerate(allTerms):
	if not term in synonyms and not term.startswith('^') and not isinWhitelist(term,whitelist):
		print str(i) + "/" + str(len(allTerms)), ":Detecting synonyms for \"" + term + "\" from", allTerms[term]['resourcenames']
		cursyms =  allTerms[term]['synonyms'] = filter(lambda x: areSimilar(term,x) and term != x and not isinWhitelist(x, whitelist), allTerms)
		for synonym in cursyms:
			if not isinWhitelist(synonym, whitelist):
				print "> \"" + synonym + "\" from", allTerms[synonym]['resourcenames']
				allTerms[term]['resourcenames'] |= allTerms[synonym]['resourcenames']
		synonyms.extend(cursyms)
	else:
		allTerms[term]['synonyms'] = []
	allTerms[term]['resourcenames'] = list(allTerms[term]['resourcenames'])
	if isinWhitelist(term,whitelist):
		print "Whitelisted term", term, "used as-is"
print len(synonyms), "synonym(s) detected"

# remove synoyms
for synonym in synonyms:
	allTerms.pop(synonym)

print len(allTerms), "term(s) left"

print "Final cleaning of plural/singular issue..."
replacements = []
for i, term in enumerate(allTerms):
	try:
		if not isinWhitelist(term, whitelist) and (p.singular_noun(term)) and not term.endswith('ss'):
			replacements.append((term, p.singular_noun(term)))
	except Exception:
		pass



print "Resolving singular/plural issues...", len(replacements)

for (oldTerm, newTerm) in replacements:
	allTerms[newTerm] = dict(resourcenames=allTerms[oldTerm]['resourcenames'], synonyms=allTerms[oldTerm]['synonyms'])
	if not oldTerm in allTerms[newTerm]['synonyms']:
		allTerms[newTerm]['synonyms'].append(oldTerm)
	if newTerm in allTerms[newTerm]['synonyms']:
		allTerms[newTerm]['synonyms'].remove(newTerm)
	del allTerms[oldTerm]
	print oldTerm, "replaced by", newTerm

print len(allTerms), "All done!"

lmtzr = WordNetLemmatizer()
stemmedData = {}
for i, term in enumerate(allTerms):
	termDict = dict(resourcenames=allTerms[term]['resourcenames'])
	synonyms = allTerms[term]['synonyms']
	if not term in synonyms:
		synonyms.append(term)
	termDict['synonyms'] = synonyms
	if isAbb(term) or isinWhitelist(term, whitelist):
		stemmedData[term] = termDict
	else:
		termtokens = map(lambda t: lmtzr.lemmatize(t).lower() , nltk.wordpunct_tokenize(term))
		stemmedTerm = (" ".join(termtokens)).replace(" - ","-")
		stemmedData[stemmedTerm] = termDict


# save new index and metadata index
writer = csv.writer(open(sys.argv[1]  + sys.argv[-4], "write"))
for i, term in enumerate(allTerms):
	writer.writerow([term])
f = open(sys.argv[1]  + sys.argv[-3], 'write')
f.write(json.dumps(stemmedData))
if sys.argv[-1] != "nocrosscut":
	ccwriter = csv.writer(open(sys.argv[1] + sys.argv[-1], "write"),  delimiter=";")
	ccwriter.writerow(["Term"] + sys.argv[3:-5])
	for i, term in enumerate(allTerms):
		ccwriter.writerow([term] + (map(lambda x: x in allTerms[term]['resourcenames'], sys.argv[3:-5])))
	writer = csv.writer(open(sys.argv[1] + "changedByPatternAll.csv", "write"))
	for term in changedByPattern:
		if not isinWhitelist(term[0],whitelist):
			writer.writerow(term)
