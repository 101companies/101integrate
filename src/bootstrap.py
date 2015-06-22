#!/usr/bin/env python
#coding=utf-8

# Generates a config for all existing books
import sys
import os
sys.path.insert(0, './mining')
import bookDownloader
import json


def get_immediate_subdirectories(dir):
	return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

lastAll = ''
lastLinked = ''
try:
  for l in open('Makefile.vars','r').readlines():
      if lastAll and lastLinked:
	  break
      elif l.startswith('ALL_BOOKS'):
	  lastAll = l.replace('ALL_BOOKS = ','')
      elif l.startswith('LINKED_BOOKS'):
	  lastLinked = l.replace('LINKED_BOOKS = ','')
except IOError:
  pass
      
allBooks = []
linkedBooks = []
nonLinkedBooks = []
if len(sys.argv) == 1:
  allBooks = get_immediate_subdirectories('../data/perbook')
else:
  allBooks = bookDownloader.selectBooks(sys.argv[1:],json.loads(open("./mining/config/config.json").read()))
for bookDir in allBooks:
  print bookDir
  if os.path.exists('../data/perbook/' + bookDir + '/contents'):
    linkedBooks.append(bookDir)
  else:
    nonLinkedBooks.append(bookDir)

with open ('Makefile.vars', 'w') as f: 
  f.write('#List of available Books about '+str(sys.argv[1:]))
  f.write('\r\nALL_BOOKS = ' + ' '.join(allBooks))
  f.write('\r\n#currently downloaded books')
  f.write('\r\nLINKED_BOOKS = ' + ' '.join(linkedBooks))
  f.write('\r\n#not-downloaded Books')
  f.write('\r\nNON_LINKED_BOOKS = ' + ' '.join(nonLinkedBooks))
  f.write('\r\n#last run processed books')
  f.write('\r\nLASTRUN_ALL = '+ lastAll)
  f.write('\r\nLASTRUN_LINKED = '+ lastLinked)
