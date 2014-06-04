#!/usr/bin/env python
#coding=utf-8

import simplejson as json
import sys

def nameIsIn(compared, strings):
  compared = normalizeString(compared)
  for s in strings:
    if (compared == normalizeString(s)):
      return True
  return False


def normalizeString(string):
  return string.strip(" :.-").lower()

def nameEquals(string1, string2):
  return (normalizeString(string1) == normalizeString(string2))

books = set();

bookData = json.loads(open("config/config.json", 'rb').read())



if nameEquals("all", sys.argv[1]):
  for data in bookData:
    books.add(data)
else:
  for arg in sys.argv:
    print " comparing " + arg
    for data in bookData:
      print "\t with " + data
      if (data != "OnlyIndex"): # has to be excluded as being no book
	#if (arg  == data  or arg == bookData[data]['fullName'] or arg == bookData[data]['title']  or arg in bookData[data]['package']): 
	if(nameIsIn(arg, ([data, bookData[data]['fullName'],bookData[data]['title']]+bookData[data]['package']))):
	  print "\t\t"+ arg+" recognized"
	  books.add(data)
	  print "\t\t"+ data+" added "
print "Books to be downloaded:"
print books
#TODO calling CRAWLER with books as args