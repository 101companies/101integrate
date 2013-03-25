#!/usr/bin/env python
#coding=utf-8

import sys
import os
import urllib
import urllib2
import json
from asq.initiators import query
from mako.template import Template

root = sys.argv[1]
resourcebase = root + sys.argv[2]
mapping = json.loads(open(resourcebase + 'mapping.json', 'rb').read())
mappedTerms = set()
for resource in mapping:
	mappedTerms |= set(filter(lambda term: not ':' in term, mapping[resource].keys()))

print 'Loading JSON dump...'
data = urllib2.urlopen('http://data.101companies.org/dumps/Wiki101Full.json')
wikidump = json.load(data)
pages = wikidump['wiki']['pages']

def handlePrefix(p):
	return p.lower() if p else ''

def createTable(contribs, classification, classname):
	classificationBase = root + classification + '/'
	classBase = classificationBase + classname
	if not os.path.exists(classificationBase):
		os.makedirs(classificationBase)
	if not os.path.exists(classBase):
		os.makedirs(classBase)
	level0Links = {}
	level1Links = {}
	for contribName in sorted(contribs.keys()):
		print 'Checking', contribName, '...'
		clevel0Links = contribs[contribName]
		level0Links[contribName] = clevel0Links
		clevel1Links = []
		print '', str(len(clevel0Links)), 'level 0 links found.'
		print ' Finding level 1 links...'
		for rawlink in clevel0Links:
			split = rawlink.split('::')[-1].replace('_',' ').split(':')
			n = split[-1].lower()
			p = split[0].lower() if len(split) > 1 else ''
			ls = query(pages).\
				where(lambda page: handlePrefix(page['page']['page']['p']) == p.lower() and page['page']['page']['n'].lower() == n and 'internal_links' in page['page']). \
				select(lambda page: map(lambda l: l.split('::')[-1].lower(),page['page']['internal_links'])). \
			to_list()
			clevel1Links.extend(ls[0] if ls else [])
		level1Links[contribName] = clevel1Links
		print '', str(len(clevel1Links)), 'level 1 links found.'
	mytemplate = Template(filename='coverageTemplate.txt')
	table = mytemplate.render(mappedTerms=mappedTerms, contribs=contribs.keys(), level0Links = level0Links, level1Links=level1Links)
	with open(classBase + '/coverage.html', 'write') as tablef:
		tablef.write(table)

allThemeInstances = query(pages).where(lambda page: ('instanceOf' in page['page']) and (filter(lambda p: p['p'] == 'Theme', page['page']['instanceOf']))).to_list()
allLanguageUsers = query(pages).where(lambda page: ('uses' in page['page']) and (filter(lambda p: p['p'] == 'Language', page['page']['uses']))).to_list()
themes = ['Haskell_data', 'Haskell_genericity ', 'Haskell_potpourri', 'Haskell_introduction']
languages = ['Haskell']

for theme in themes:
	print 'Table for', theme
	contribs = query(allThemeInstances). \
  	where(lambda page: filter(lambda p: p['p'] == 'Theme' and p['n'] == theme and 'internal_links' in page['page'], page['page']['instanceOf'])). \
  	select(lambda page: {'name': page['page']['page']['n'], 'links': page['page']['internal_links']}). \
  	to_list()
  	createTable(dict([(c['name'],c['links']) for c in contribs]), 'themes', theme)

for language in languages:
 	print 'Table for', theme
	contribs = query(allLanguageUsers). \
  	where(lambda page: filter(lambda p: p['p'] == 'Language' and p['n'] == language and 'internal_links' in page['page'], page['page']['uses'])). \
  	select(lambda page: {'name': page['page']['page']['n'], 'links': page['page']['internal_links']}). \
  	to_list()
  	createTable(dict([(c['name'],c['links']) for c in contribs]), 'languages', language)

