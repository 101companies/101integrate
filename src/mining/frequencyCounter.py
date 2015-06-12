import csv
import os
import sys
import re
import simplejson as json
import csv
from collections import defaultdict
import inflect
p = inflect.engine()
import logging
import logging.config

def allindices(string, sub):
    return [match.start() for match in re.finditer(re.escape(sub), string)]

def getLine(index, content): return len((content[:index + 1]).splitlines()) - 1

def calculateFreqContext(content, term, info):
	pterm = p.plural(term)
	sinf = content.count(term)#len([(a.start(), a.end()) for a in list(re.finditer(term, content))])
	pluf = content.count(pterm)#len([(a.start(), a.end()) for a in list(re.finditer(pterm, content))])
	return (sinf + pluf)

def calculateFreqFolder(path, term):
	listing = os.listdir(path)
	freq = 0
	pop = []
	for infile in listing:
		if not os.path.isdir(infile) and not infile.startswith("."):
			f = open(path+infile,"read")
			content = f.read()
			n = 0
			curfreq = calculateFreqContext(content, term, path+infile)
			freq = freq + curfreq
			pop.append(curfreq)
	return dict(freq=freq, pop=pop)

def main():
	# read index file
	#indexReader = csv.reader(open(sys.argv[1], 'rb'), delimiter=',')
	resInfos = json.loads(open("config/config.json", 'rb').read())
	res = resInfos["OnlyIndex"]
	indexReader = csv.reader(open(res['kind']+"/"+res['folder'] + "/" +res['index'], 'rb'), delimiter=',')
	dicts = {}
	for resName2 in resInfos:
		res2 = resInfos[resName2]
		if res2['kind'] != "OnlyIndex":
			dicts[res2['title']] = defaultdict(int)
	terms = []
	for row in indexReader:
		terms.append(row[0].partition("!")[0])
		af = row[0].partition("!")[2]
		if af != '':
			terms.append(af)
	terms.append("class=\"function\"")
	result = {}
	resNames = []
	if res['kind'] == "OnlyIndex":
		pop = {}
		for resName7 in resInfos:
			if resInfos[resName7]['kind'] != "OnlyIndex":
				pop[resInfos[resName7]['title']] = {}
	for term in terms:
		fs = {}
		logging.info('Processing "' + term + '" from index of ' + res['title'])
		for resName3 in resInfos:
			res3 = resInfos[resName3]
			if res3['kind'] != "OnlyIndex":
				resNames = list(set(resNames + [resName3]))
				logging.info("Processing folder", res3['kind']+"/"+res3['folder'])
				cur =  calculateFreqFolder(res3['kind']+"/"+res3['folder'] + "/" + 'data/',term)
				fs[res3['title']] = dicts[res3['title']][term] = cur['freq']
				if res['kind'] == "OnlyIndex":
					pop[res3['title']][term] = cur['pop']
		result[term] = fs
	html = "<h1>Term frequencies for index of " + res['title'] + "</h1><table border=\"1\">" + "<tr>" + "<th><b>Term</b></th>"
	for resName4 in resInfos:
		res4 = resInfos[resName4]
		if res4['kind'] != "OnlyIndex":
			html = html + "<th><b>" + res4['title'] + "</b></th>"
	order = []
	if res['kind'] != "OnlyIndex":
		order = sorted(dicts[res['title']], key=dicts[res['title']].get, reverse=True)
	else:
		for resName6 in resInfos:
			res6 = resInfos[resName6]
			if res6['kind'] != "OnlyIndex":
				order = sorted(dicts[res6['title']], key=dicts[res6['title']].get, reverse=True)
	for term in order:
		html = html +  "<tr><td>" + term + "</td>"
		for resName5 in resInfos:
			res5 = resInfos[resName5]
			if res5['kind'] != "OnlyIndex":
				html = html +  "<td>" + str(dicts[res5['title']][term]) + "</td>"
		html = html + "</tr>"
	html = html + "</tr></table>"
	f = open(res['kind']+"/"+res['folder'] + "/" +"frequencies.json","write")
	f.write(json.dumps(result), indent = "\t")
	w = csv.writer(open(res['kind']+"/"+res['folder']+ "/"+'frequencies.csv', 'wb'), delimiter=';')
	w.writerow(["Term"] + resNames)
	for key, value in result.items():
		r = [key] + value.values()
		w.writerow(r)
	f2 = open(res['kind']+"/"+res['folder']+ "/"+"frequencies.html","write")
	f2.write(html)
	if res['kind'] == "OnlyIndex":
		for resName9 in resInfos:
			res9 = resInfos[resName9]
			if res9['kind'] != "OnlyIndex":
				w2 = csv.writer(open(res9['kind'] + "/" + res9['folder'] + "/" + "popularity.csv", 'wb'), delimiter=";")
				curpop = pop[res9['title']]
				header = ['Term']
				listing = os.listdir(res9['kind'] + "/" + res9['folder'] + "/data/")
				for infile in listing:
					if os.path.isdir(infile) == False and infile.partition(".")[0] != "":
						header.append(infile.partition(".")[0])
				w2.writerow(header)
				for term in terms:
					termpoprow = [term]
					termpop = curpop[term]
					termpoprow.extend(termpop)
					w2.writerow(termpoprow)

if __name__ == "__main__":
	logging.config.fileConfig('../config/pythonLogging.conf'.replace('/',os.path.sep))
	main()
