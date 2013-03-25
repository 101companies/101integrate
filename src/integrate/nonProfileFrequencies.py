#!/usr/bin/env python
#coding=utf-8

import sys
import csv
import json
from mako.template import Template

resoucebase = sys.argv[1]
mainresource = sys.argv[2]
resources =  sys.argv[3:]
profiledTerms = set([])
for resource in resources:
	profile = csv.reader(open(resoucebase + resource + '/chapterProfile.numbers.csv'), delimiter=',')
	for row in profile:
		profiledTerms.add(row[1])
frequencies = json.loads(open(resoucebase + mainresource + "/frequencies.json", 'rb').read())
mytemplate = Template(filename='frequenciesTemplate.txt')
nonProfileTerms = filter(lambda f: f not in profiledTerms, frequencies)
table = mytemplate.render(frequencies=frequencies, nonProfileTerms=nonProfileTerms)
with open(resoucebase + mainresource + '/nonProfileFrequencies.html', 'write') as tablef:
		tablef.write(table)
