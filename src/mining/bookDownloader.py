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

bookData = json.loads(open("config/config.json", 'rb').read()) #TODO read as hirachical object
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
      if (arg  == data ): # or arg == data.fullname or arg in data.package): 
	print "\t\t"+ arg+" recognized"
	books.add(data)
	print "\t\t"+ data+" added "
	
print "Books to be downloaded:"
print books
#TODO calling CRAWLER with books as args