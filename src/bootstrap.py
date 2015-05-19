#!/usr/bin/env python
#coding=utf-8

# Generates a config for all existing books
import sys
import os
sys.path.insert(0, './mining')
import bookDownloader
import json
import logging #needed for nunning the whole project in debug/info-mode

allBooks = []
def get_immediate_subdirectories(dir):
	return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

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
  f.write ('#List of available Books about '+str(sys.argv[1:])+'  \r\n ALL_BOOKS = ' + ' '.join(allBooks) + '\n#currently downloaded books\nLINKED_BOOKS = ' + ' '.join(linkedBooks) + '\n#not-downloaded Books \nNON_LINKED_BOOKS = ' + ' '.join(nonLinkedBooks))