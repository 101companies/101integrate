#!/usr/bin/env python
#coding=utf-8

import json
import urllib2
import asq
from asq.initiators import query

data = urllib2.urlopen('http://data.101companies.org/dumps/Wiki101Full.json')

wikidump = json.load(data)
pages = wikidump['wiki']['pages']

allThemeInstances = query(pages).where(lambda page: ('instanceOf' in page['page']) and (filter(lambda p: p['p'] == 'Theme', page['page']['instanceOf']))).to_list()

haskellThemes = ['Data_modeling_with_Haskell', 'Generic_programming_in_Haskell', 'Haskell_potpourri']

for theme in haskellThemes:
  print theme + '\n'
  terms = query(allThemeInstances). \
  where(lambda page: filter(lambda p: p['p'] == 'Theme' and p['n'] == theme, page['page']['instanceOf'])). \
  select(lambda page: { 'contribution' : page['page']['page']['n'], 'concepts': filter(lambda term: not ':' in term , page['page']['internal_links']) }). \
  to_list()
  print terms