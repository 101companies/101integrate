#!/usr/bin/env python
#coding=utf-8

# Generates a config for all existing books
import sys
import os
from mining import bookDownloader
import json


def get_immediate_subdirectories(dir):
	return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]
 
def bootstrap(resources="",useNonLinkables=False):
	allBooks = []
	linkedBooks = []
	nonLinkedBooks = []
	config = json.loads(open("./config/config.json","r").read())
	if not resources:
		allBooks = list(config.keys())
		allBooks.remove("OnlyIndex")
	else:
		allBooks = bookDownloader.selectBooks([resources],config)
	if not useNonLinkables:
		allBooks = bookDownloader.getLinkables(allBooks,config)
	for bookDir in allBooks:
		print bookDir
		if os.path.exists('../data/perbook/' + bookDir.strip() + '/contents'):
			linkedBooks.append(bookDir)
		else:
			nonLinkedBooks.append(bookDir)

	with open ('Makefile.vars', 'w') as f: 
	  f.write('#List of available Books about '+str(resources))
	  f.write('\r\nALL_BOOKS = ' + ' '.join(allBooks))
	  f.write('\r\n#currently downloaded books')
	  f.write('\r\nLINKED_BOOKS = ' + ' '.join(linkedBooks))
	  f.write('\r\n#not-downloaded Books')
	  f.write('\r\nNON_LINKED_BOOKS = ' + ' '.join(nonLinkedBooks))

if __name__ == "__main__":
	bootstrap(*sys.argv[1:])
