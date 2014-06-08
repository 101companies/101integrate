import sys
import urllib2
import simplejson as json
import os
from bs4 import BeautifulSoup

dataPath = ".."+os.path.sep+".."+os.path.sep+"data"

def getMetaPath(book):
    return dataPath+os.path.sep+"perbook"+os.path.sep+book+os.path.sep+"metadata"+os.path.sep
  
def isRelative(url):
     if (("http://" in url) or ("https://" in url)):
       return True
     else:
       return False

if (len(sys.argv)<=1):
    print "No book specified. Aborting."
else:
    bookData = json.loads(open("config"+os.path.sep+"config.json", 'rb').read())
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    for arg in sys.argv[1:]:	
	try:
	    links = []
	    url = bookData[arg]['urlBase'].strip()
	    print "checking " + url
	    infile = opener.open(url)
	    if (infile.info()['content-type'].count('text/html') > 0):
		  doc = BeautifulSoup(infile.read())
		  for l in doc.find_all('a'):
		      info = [l, l.get('href'), l.string]
		      if((not ("mailto:" in info[1])) and 
			((not ("http:" in info[1])) or url in info [1]) and 
			(bookData[arg]['ext'] in info[1])):
			  links.append(info)
	    #print links
	    path = getMetaPath(arg)
	    chaptersWrite = open(path+"chaptersGen.txt","w")
	    for l in links:
		    #print l
		    if(isRelative(l[1])):
		      chaptersWrite.write(bookData[arg]['urlBase'].strip()+l[1])
		      print l
		    else:
		      chaptersWrite.write(l[1])
		    chaptersWrite.write("\r\n")
	except KeyError:
	    print arg + " skipped."
	else:
	    pass
	

	    
      