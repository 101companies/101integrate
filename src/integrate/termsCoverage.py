#!/usr/bin/env python
#coding=utf-8

import sys
import os
import urllib
import urllib2
import json
from asq.initiators import query
from mako.template import Template

from constants import *

root = sys.argv[1]
#root = "../../data"

resourcebase = root + sys.argv[2]
#resourcebase = "../../data/allbooks/"

def handlePrefix(p):
    return p.lower() if p else ''

def createTable(resource, contribs, classification, classname):
    classificationBase = root + classification + '/'
    classBase = classificationBase + classname.replace('_',' ')
    if not os.path.exists(classificationBase):
		os.makedirs(classificationBase)
    if not os.path.exists(classBase):
		os.makedirs(classBase)
    if not os.path.exists(classBase + "/" + resource):
        os.makedirs(classBase + "/" + resource)
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
            n = split[-1]
            p = split[0].title() if len(split) > 1 else ''
            ls = query(pages).\
				where(lambda page: handlePrefix(page['p']).lower() == p.lower() and page['n'].lower() == n.lower() and 'internal_links' in page). \
				select(lambda page: map(lambda l: l.split('::')[-1].lower(),page['internal_links'])). \
            to_list()
        clevel1Links.extend(filter(lambda l: l not in clevel0Links, ls[0]) if ls else [])
        level1Links[contribName] = clevel1Links
        print '', str(len(clevel1Links)), 'level 1 links found.'
    mytemplate = Template(filename='templates/coverageTemplate.txt')
    table = mytemplate.render(mappedTerms=mappedTerms, contribs=contribs.keys(), level0Links = level0Links, level1Links=level1Links)
    with open(classBase + "/" + resource + '/coverage.html', 'write') as tablef:
		tablef.write(table)
    coverage = {}
    for term in mappedTerms:
        coverage[term] = {}
        coverage[term]['level0'] = filter(lambda c: term.lower() in map(lambda t: t.lower(), level0Links[c]), contribs)
        coverage[term]['level1'] = filter(lambda c: term.lower() in map(lambda t: t.lower(), level1Links[c]) and not c in coverage[term]['level0'], contribs)
    with open(classBase + "/" + resource + '/coverage.json', 'write') as tablefjson:
        json.dump(coverage, tablefjson)


print 'Loading JSON dump...'
data = urllib2.urlopen('http://data.101companies.org/dumps/wiki.json')
wikidump = json.load(data)
pages = wikidump['wiki']['pages']

allThemeInstances = query(pages).where(lambda page: ('instanceOf' in page) and (filter(lambda p: p['p'] == 'Theme', page['instanceOf']))).to_list()
allLanguageUsers = query(pages).where(lambda page: ('uses' in page) and (filter(lambda p: p['p'] == 'Language', page['uses']))).to_list()

mapping = json.loads(open(resourcebase + 'mapping.json', 'rb').read())
mappedTerms = set()
for resource in mapping:
    mappedTerms |= set(mapping[resource].keys())
    print resource
    print mappedTerms

    for theme in themes:
        print 'Table for', theme
        contribs = query(allThemeInstances). \
        where(lambda page: filter(lambda p: p['p'] == 'Theme' and p['n'] == theme and 'internal_links' in page, page['instanceOf'])). \
        select(lambda page: {'name': page['n'], 'links': map(lambda l: l.lower().split('::')[-1], page['internal_links'])}). \
        to_list()
        createTable(resource, dict([(c['name'],c['links']) for c in contribs]), 'themes', theme)

    for language in languages:
        print 'Table for', language
        contribs = query(allLanguageUsers). \
  	    where(lambda page: filter(lambda p: p['p'] == 'Language' and p['n'] == language and 'internal_links' in page, page['uses'])). \
  	    select(lambda page: {'name': page['n'], 'links': map(lambda l: l.lower().split('::')[-1],page['internal_links'])}). \
  	    to_list()
        createTable(resource, dict([(c['name'],c['links']) for c in contribs]), 'languages', language)

