#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import simplejson as json

def readCSV(csvFile):
	reader = csv.reader(open(csvFile,"rb"), delimiter=',', quotechar='\"')
	return list(reader)

def main(books):
	overview = [["Book","Kind","IndexTerm","WikiTerm","Comment"]]
	stats = {}
	for b in books:
		temp = readCSV("../../data/perbook/"+b+"/metadata/mapping.csv")[1:]
		overview += [[b]+t for t in temp]
		data={}
		data['non-mapped'] = len([t for t in temp if not t[-2]])
		data['mapped'] = len([t for t in temp if t[-2]])
		data['auto-mapped'] = len([t for t in temp if t[-1] == "automatically assigned"])
		data['terms'] = sorted(list(set([t[-2] for t in temp if t[-2]])), key=(lambda x: x.lower()))
		data['wikiTerms'] = len(data['terms'])
		stats[b] = data
	writer = open("../../data/allbooks/MappingStats.json","w")
	writer.write(json.dumps(stats, indent="\t"))
	writer.close()
	f = open("../../data/allbooks/MappingStats.csv","w")
	csvwriter = csv.writer(f)
	cols = ["mapped","non-mapped","auto-mapped","wikiTerms"]
	csvwriter.writerow(["book"]+cols)
	for k in stats.keys():
		csvwriter.writerow([k]+[stats[k][i] for i in cols])
	f.close()
	f = open("../../data/allbooks/MappingOverview.csv","w")
	csvwriter = csv.writer(f)
	csvwriter.writerow(overview[0])
	for line in sorted(overview[1:], key=(lambda x: x[-2])):
		csvwriter.writerow(line)
	f.close()
	allWikiTerms = sorted(set([term for k in stats.keys() for term in stats[k]['terms']]), key=(lambda x: x.lower()))
	termBookOverview = [[t] +["X" if t in stats[k]['terms'] else "" for k in stats.keys()] for t in allWikiTerms]
	termBookOverview = [["Term"]+stats.keys()] + termBookOverview
	f = open("../../data/allbooks/wikiTermsBook.csv","w")
	csvwriter = csv.writer(f)
	csvwriter.writerows(termBookOverview)
	f.close()

if __name__ == '__main__':
	main(sys.argv[1:])
