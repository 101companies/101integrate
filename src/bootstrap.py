#!/usr/bin/env python
#coding=utf-8

# Generates a config for all existing books

import os

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

books = []
nonLinkedBooks = []
for bookDir in get_immediate_subdirectories('../data/perbook'):
  if os.path.exists('../data/perbook/' + bookDir + '/contents'):
    books.append(bookDir)
  else:
  	nonLinkedBooks.append(bookDir)
  	  	
with open ('Makefile.vars', 'w') as f: 
	f.write ('BOOKS = ' + ' '.join(books) + '\nNON_LINKED_BOOKS = ' + ' '.join(nonLinkedBooks))