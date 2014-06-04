#!/usr/bin/env python
#coding=utf-8

import simplejson as json
import sys

def normalizeString(string):
  return string.strip().strip(" ").lower()

def nameEquals(string1, string2):
  if(normalizeString(string1) == normalizeString(string2)):
    return True
  else:
    return False

books = set();

bookData = json.loads(open("config/config.json", 'rb').read())
print "read config:"
print bookData

if nameEquals("all", sys.argv[1]):
  for data in bookData:
    books.add(data)
else:
  for arg in sys.argv:
    print " comparing " + arg
    for data in bookData:
      print "\t with " + data
      print bookData[data]
      print bookData[data].items()
      print type(bookData[data])
      if (arg  == data  or arg == bookData[data]['fullName'] or arg == bookData[data]['title']  or arg in bookData[data]['package']): 
	print "\t\t"+ arg+" recognized"
	books.add(data)
	print "\t\t"+ data+" added "
	
print "Books to be downloaded:"
books.discard("OnlyIndex")
print books
#TODO calling CRAWLER with books as args