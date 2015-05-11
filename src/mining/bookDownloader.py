import json
import sys
import os
import crawler
import constants
import re


##
#@param compared	the string to be compared
#@param strings		an array of strings which are compared with the compared
#@return 	wether the compared matches another sting in "normal form"
def nameIsIn(compared, strings):
  compared = normalizeString(compared)
  for s in strings:
    if (compared == normalizeString(s)):
      return True
  return False



##
#@param	string	a String
#@return	a normalized Representation of this string
def normalizeString(string):
    return re.sub("[^\w]", "", string).lower()






##
#@param		args	the books you want to download
#@param 	config	the configuration
#@return	a set containg books matching with args
def selectBooks(args, config):
  books = set();
  bookData = config

  if (nameIsIn("all",[args[0]]) or len(args) == 0 ):
    for data in bookData:
	try:
	    print bookData[data]['fullName'] # SKIP NONBOOKS
	    if bookData[data]['isLinkable']:
	      books.add(data)
	except KeyError:
	    print "\t "+data + " skipped."
	else:
	    pass
  else:
    for arg in args:
	print " comparing " + arg
	for data in bookData:
	    try:
		  print "\t with " + data
		  if(nameIsIn(arg, ([data, bookData[data]['fullName'],bookData[data]['title']]+bookData[data]['tag'])) and bookData[data]['isLinkable']):
		      print "\t\t"+ arg+" recognized"
		      books.add(data)
		      print "\t\t"+ data+" added "
	    except KeyError:
		  print "\t "+data + " skipped."
	    else:
		  pass
		
  return books



##
#@param	books		the books you want to download
#@param bookfldr	the folder in which the book should be downloaded
# downloads te specified books in the specified folder
def downloadBooks(books, bookfldr):
  print "Books to be downloaded:"
  print books
  if bookfldr[len(bookfldr)-1] is not ("/" or os.path.sep):
      bookfldr += os.path.sep
  bookfldr = bookfldr.replace("/",os.path.sep)
  for b in books:
      constants.mkdir((bookfldr+b+os.path.sep+"contents"))
      crawler.crawl(b,bookfldr)
  
  
    
    
if __name__ == "__main__":
   downloadBooks(selectBooks(sys.argv[1:], json.loads(open(constants.configPath, 'rb').read())),constants.bookPath)
