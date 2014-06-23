import simplejson as json
import sys
import os

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
    return string.lower().replace(" ","").replace(":","").replace("-","").replace(".","")







books = set();
bookData = json.loads(open("config"+os.path.sep+"config.json", 'rb').read())

if (nameIsIn("all",[sys.argv[1]]) or len(sys.argv) ==1 ):
    for data in bookData:
	try:
	    print bookData[data]['fullName'] # SKIP NONBOOKS	
	    books.add(data)
	except KeyError:
	    print "\t "+data + " skipped."
	else:
	    pass
else:
    for arg in sys.argv[1:]:
	print " comparing " + arg
	for data in bookData:
	    try:
		  print "\t with " + data
		  if(nameIsIn(arg, ([data, bookData[data]['fullName'],bookData[data]['title']]+bookData[data]['package'])) and bookData[data]['isLinkable']):
		      print "\t\t"+ arg+" recognized"
		      books.add(data)
		      print "\t\t"+ data+" added "
	    except KeyError:
		  print "\t "+data + " skipped."
	    else:
		  pass
		

print "Books to be downloaded:"
print books


for b in books:
  try:
      os.makedirs(("../../data/perbook/"+b+"/contents").replace("/",os.path.sep))
  except OSError:
      pass
  else:
      pass
  sys.argv = [sys.argv[0],b,("../../data/perbook/").replace("/",os.path.sep)]
  import crawler
  #print subprocess.Popen("python crawler.py "+b+" ../../data/perbook/".replace("/",os.path.sep), shell = True).wait()