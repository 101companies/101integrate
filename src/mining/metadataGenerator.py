import sys
import urllib2
import simplejson as json
from bs4 import BeautifulSoup

dataPath = "../../data"

if (len(sys.argv)<=1):
    print "No book specified. Aborting."
else:
    bookData = json.loads(open("config/config.json", 'rb').read())
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    for arg in sys.argv[1:]:
	links = []
	try:
	    url = bookData[arg]['urlBase'].strip() # + bookData[arg]['ext']
	    print "checking " + url
	    infile = opener.open(url)
	    if (infile.info()['content-type'].count('text/html') > 0):
		  doc = BeautifulSoup(infile.read())
		  for l in doc.find_all('a'):
		      info = [l, l.get('href'), l.string]
		      #print info[1]
		      if((not ("mailto:" in info[1])) and (not ("http:" in info[1])) and (bookData[arg]['ext'] in info[1])):
			  links.append(info)
	    print links
	except KeyError:
	    print arg + " skipped."
	else:
	    pass
	
	#for l in links:
	    
      