#!/usr/bin/env python
#coding=utf-8

import sys
import csv
import json
from mako.template import Template
import logging #needed for nunning the whole project in debug/info-mode

root = sys.argv[1]
allbooksbase =root + sys.argv[2]
resoucebase = root + sys.argv[3]
mainresource = sys.argv[4]
resources =  sys.argv[5:]
profiledTerms = set([])
rank = {}
rawrank = csv.reader(open(allbooksbase + '/rank.csv', 'rU'), delimiter=',')
for row in rawrank:
	rank[row[0]] = row[1]

for resource in resources:
	profile = csv.reader(open(resoucebase + resource + '/chapterProfile.numbers.csv'), delimiter=',')
	for row in profile:
		profiledTerms.add(row[1])
frequencies = json.loads(open(resoucebase + mainresource + "/frequencies.json", 'rb').read())
mytemplate = Template(filename='templates/frequenciesTemplate.txt')
nonProfileTerms = filter(lambda f: f not in profiledTerms, frequencies)
table = mytemplate.render(frequencies=frequencies, nonProfileTerms=nonProfileTerms, rank=rank)
with open(resoucebase + mainresource + '/nonProfileFrequencies.html', 'write') as tablef:
		tablef.write(table)
