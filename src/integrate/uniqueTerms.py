#!/usr/bin/env python
#coding=utf-8

# Unique terms for the documentation and the textbooks
# See https://github.com/101companies/101integrate/issues/20

from constants import *
import csv
import itertools
import json
import os
import urllib2
from asq.initiators import query

# returns distinct values from list
# see http://www.peterbe.com/plog/uniqifiers-benchmark
def distinct(seq):
  noDupes = []
  [noDupes.append(i) for i in seq if not noDupes.count(i)]
  return noDupes

data = urllib2.urlopen('http://data.101companies.org/dumps/Wiki101Full.json')
wikidump = json.load(data)
pages = wikidump['wiki']['pages']

allThemeInstances = query(pages).where(lambda page: ('instanceOf' in page['page']) and (filter(lambda p: p['p'] == 'Theme', page['page']['instanceOf']))).to_list()

wikiConpepts = []
for theme in themes:
  concepts = query(allThemeInstances). \
    where(lambda page: filter(lambda p: p['p'] == 'Theme' and p['n'] == theme and 'internal_links' in page['page'], page['page']['instanceOf'])). \
    select(lambda page: page['page']['internal_links']). \
    to_list()

  wikiConpepts.append(c.capitalize() for c in list(itertools.chain.from_iterable(concepts)))

distinctWikiConcepts =  filter(lambda term: term.startswith("Language") or term.startswith("Technology") or (not ':' in term), distinct(list(itertools.chain.from_iterable(wikiConpepts))))  	
#print distinctWikiConcepts

bookConcepts = []
for book in books:
  if (os.path.exists('../../data/perbook/' + book + '/metadata/mapping.csv') == False):
    pass
  else:  
    ifile  = open('../../data/perbook/' + book + '/metadata/mapping.csv', 'rb')
    reader = csv.reader(ifile)
    reader.next() # skip header
    for row in reader:
      if (row[2] != ''):
        bookConcepts.append(row[2]) # wikiterm

distinctBookConcepts = distinct(bookConcepts)
#print distinctBookConcepts

def getUniqueConcepts(input, sourceToSearch):
  unique = []
  for concept in input:
    if concept in sourceToSearch:
      pass
    else:
      unique.append(concept)

  return unique          

wikiOnly = getUniqueConcepts(distinctWikiConcepts, distinctBookConcepts)
booksOnly = getUniqueConcepts(distinctBookConcepts, distinctWikiConcepts)

#print "Wiki only"
#print wikiOnly

#print "Books only"
#print booksOnly
#print json.dumps({'wikiOnly': wikiOnly, 'booksOnly': booksOnly})

with open ('../../data/summary/wikiOnly.tex', 'w') as f: 
  f.write(',\n'.join(map(lambda x: "\wikipage{" + x + "}",  wikiOnly)))

with open ('../../data/summary/booksOnly.tex', 'w') as f: 
  f.write(',\n'.join(map(lambda x: "\wikipage{" + x + "}",  booksOnly)))  





