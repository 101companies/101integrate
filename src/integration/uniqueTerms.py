#!/usr/bin/env python
#coding=utf-8

# Unique terms for the documentation and the textbooks
# See https://github.com/101companies/101integrate/issues/20

from constants import *
import csv
import itertools
import simplejson as json
import os
import urllib2
from asq.initiators import query
from jinja2 import Environment, FileSystemLoader
import sys
import logging
import logging.config

env = Environment(line_statement_prefix='#', loader=FileSystemLoader('templates'), trim_blocks=True)
sorter = lambda x: x.lower()

# terms contributed uniquely by each textbook
def getUniqueContributionPerBook(bookConcepts):
	res = {}
	for term, books in bookConcepts.items():
		books = list(books)
		# unique term - defined only in one book
		if (len(books) == 1):
			if (res.has_key(books[0]) == False):
				res[books[0]] = []
			res[books[0]].append(term)
	return res

def getNonUniqueContributionFromBooks(bookConcepts):
	res = []
	for term, books in bookConcepts.items():
		books = list(books)
		# non-unique term - defined more than in one book
		if (len(books) > 1):
			res.append(term)
	return distinct(res)

def getUniqueConcepts(input, sourceToSearch):
	unique = []
	for concept in input:
		if not (concept in sourceToSearch):
			unique.append(concept)
	return unique


# returns distinct values from list
# see http://www.peterbe.com/plog/uniqifiers-benchmark
def distinct(seq):
	noDupes = []
	[noDupes.append(i) for i in seq if not noDupes.count(i)]
	return [d for d in noDupes if d]#removes empty values


def main(books):
	data = urllib2.urlopen('http://data.101companies.org/dumps/wiki.json')
	wikidump = json.load(data)
	pages = wikidump['wiki']['pages']
	allBookConcepts = []
	bookConcepts = {}
	#books = sys.argv[1:]
	wikiConcepts = []

	allThemeInstances = query(pages).where(lambda page: ('instanceOf' in page) and (filter(lambda p: p['p'] == 'Theme', page['instanceOf']))).to_list()
	for theme in themes:
		concepts = query(allThemeInstances).where(lambda page: filter(lambda p: p['p'] == 'Theme' and p['n'] == theme and 'internal_links' in page, page['instanceOf'])).select(lambda page: page['internal_links']).to_list()
		wikiConcepts.append(c.capitalize() for c in list(itertools.chain.from_iterable(concepts)))

	distinctWikiConcepts =  filter(lambda term: term.startswith("Language") or term.startswith("Technology") or (not ':' in term), distinct(list(itertools.chain.from_iterable(wikiConcepts))))
	logging.debug("distinct wiki-concepts:"+str(distinctWikiConcepts))

	for book in books:
		if (os.path.exists('../../data/perbook/' + book + '/metadata/mapping.csv')):
			ifile  = open('../../data/perbook/' + book + '/metadata/mapping.csv', 'rb')
			reader = csv.reader(ifile)
			reader.next() # skip header
			for row in reader:
				term = str(row[2])
				if (term != ''):
					allBookConcepts.append(term) # wikiterm
				if not bookConcepts.has_key(term):
					bookConcepts[term] = set()
				bookConcepts[term].add(book)

	logging.debug("book-concepts: "+str(bookConcepts))
	distinctBookConcepts = distinct(allBookConcepts)
	logging.debug("distinct book-concepts: "+str(distinctBookConcepts))


	unique = getUniqueContributionPerBook(bookConcepts)
	nonUnique  = getNonUniqueContributionFromBooks(bookConcepts)

	wikiOnly = getUniqueConcepts(distinctWikiConcepts, distinctBookConcepts)
	booksOnly = getUniqueConcepts(distinctBookConcepts, distinctWikiConcepts)

	logging.debug("Wiki only")
	logging.debug(wikiOnly)

	logging.debug("Books only")
	logging.debug(booksOnly)
	#print json.dumps({'wikiOnly': wikiOnly, 'booksOnly': booksOnly})


	for book, terms in unique.items():
		toTex(terms, str(book) + '_unique.tex')
		toJson(terms, str(book) + '_unique.json')
		toHtml(terms, str(book) + '_unique.html')

	toTex(nonUnique, 'nonUnique.tex')
	toJson(nonUnique, 'nonUnique.json')
	toHtml(nonUnique, 'nonUnique.html')

	toTex(wikiOnly, 'wikiOnly.tex')
	toJson(wikiOnly, 'wikiOnly.json')
	toHtml(wikiOnly, 'wikiOnly.html')

	toTex(booksOnly, 'booksOnly.tex')
	toJson(booksOnly, 'booksOnly.json')
	toHtml(booksOnly, 'booksOnly.html')

	toTex(distinctWikiConcepts, 'wiki.tex')
	toJson(distinctWikiConcepts, 'wiki.json')
	toHtml(distinctWikiConcepts, 'wiki.html')

	toTex(distinctBookConcepts, 'books.tex')
	toJson(distinctBookConcepts, 'books.json')
	toHtml(distinctBookConcepts, 'books.html')

def toTex(list, file):
	with open ('../../data/summary/'+ file, 'w') as f:
		f.write(',\n'.join(map(lambda x: "\wikipage{" + x + "}",  sorted(list, key=sorter))))

def toJson(list, file):
	with open ('../../data/summary/'+ file, 'w') as f:
		f.write(json.dumps(sorted(list, key=sorter), indent="\t"))

def toHtml(list, file):
	list = sorted(list, key=sorter)
	# Open and read template
	t = env.get_template('table.html')
	output = t.render(list = list)
	# Write the output to a file
	with open('../../data/summary/'+ file, 'w') as out_f:
		out_f.write(output)


if __name__ =="__main__":
	logging.config.fileConfig('../config/pythonLogging.conf')
	main(sys.argv[1:])

