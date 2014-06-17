import simplejson as json
import sys
import subprocess32 as subprocess
import os

def nameIsIn(compared, strings):
  compared = normalizeString(compared)
  for s in strings:
    if (compared == normalizeString(s)):
      return True
  return False


def normalizeString(string):
    return string.lower().replace(" ","").replace(":","").replace("-","").replace(".","")

def nameEquals(string1, string2):
    return (normalizeString(string1) == normalizeString(string2))






books = set();
bookData = json.loads(open("config"+os.path.sep+"config.json", 'rb').read())

if (nameEquals("all", sys.argv[1]) or len(sys.argv) ==1 ):
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
  print subprocess.Popen("python crawler.py "+b+" ../../data/perbook/".replace("/",os.path.sep), shell = True).wait()