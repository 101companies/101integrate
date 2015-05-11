#!/usr/bin/env python
#coding=utf-8

# Generates a config for all existing books

import os

allBooks = []
def get_immediate_subdirectories(dir):
	return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

linkedBooks = []
nonLinkedBooks = []
allBooks = get_immediate_subdirectories('../data/perbook')
for bookDir in allBooks:
  print bookDir
  if os.path.exists('../data/perbook/' + bookDir + '/contents'):
    linkedBooks.append(bookDir)
  else:
    nonLinkedBooks.append(bookDir)

with open ('Makefile.vars', 'w') as f: 
  f.write ('#List of available Books \r\n'+'#downloadable books \nALL_BOOKS = ' + ' '.join(allBooks) + '\n#currently downloaded books\nLINKED_BOOKS = ' + ' '.join(linkedBooks) + '\n#not-downloaded Books \nNON_LINKED_BOOKS = ' + ' '.join(nonLinkedBooks))