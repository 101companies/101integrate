import sys
import urllib2
import simplejson as json
import os
import re
from bs4 import BeautifulSoup

dataPath = ".."+os.path.sep+".."+os.path.sep+"data"

def getMetaPath(book):
    path = dataPath+os.path.sep+"perbook"+os.path.sep+book+os.path.sep+"metadata"+os.path.sep
    try:
      os.makedirs(path)
      print path + "was created"
    except OSError:
      pass
    else:
      pass
    return path





def isRelative(url):
     #return (not (("http://" in url) or ("https://" in url)))
     return (re.match("http(s)?://", url) is not None)



#DEPRECATED replaced with acceptor
def isAccepted(url, ext):
    return (not ("mailto:" in url) and ((not ("http:" in url)) or url in url) and (ext in url))





def createAcceptor(urlBase, ext):
    regex=""
    for url in urlBase.replace(".","\.").split("/"):
	regex += ("("+url+"/)?")
    regex += "/?"+"((-|_|[A-Za-z0-9])*/?){1,2}"+ext.replace(".","\.")
    print regex
    return re.compile(regex)





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
	    print "Regex-Term:"
	    acceptor = createAcceptor(url, bookData[arg]['ext'])
	    print "checking " + url
	    infile = opener.open(url)
	    if (infile.info()['content-type'].count('text/html') > 0):
		  doc = BeautifulSoup(infile.read())
		  for l in doc.find_all('a'):
		      info = [l, l.get('href'), l.string]
		      if info[1] is not None:
			  if acceptor.match(info[1]) is not None:
			      links.append(info)
	    print "collected Information"
	    path = getMetaPath(arg)
	    chaptersWrite = open(path+"chaptersGen.txt","w")
	    chapters = []
	    print "Processing links"
	    for l in links:
		    print l
		    if isRelative(l[1]):
		      chaptersWrite.write(url+l[1])
		      filename = l[1]+".txt"
		      chapters.append({"file": filename ,"title": l[2]})
		    else:
		      temp = l[1].split(os.path.sep)
		      filename = temp[len(temp)-1]+".txt"
		      chapters.append({"file": filename,"title": l[2]})
		      chaptersWrite.write(l[1])
		    chaptersWrite.write("\r\n")
	    chaptersWrite.close()
	    chaptersWriteJSON = open(path+"chaptersGen.json","w")
	    chaptersWriteJSON.write(json.dumps({"chapters": chapters}, indent="\t"))
	    chaptersWriteJSON.close()
	    print "Metadata generated"
	except KeyError:
	    print arg + " skipped."
	else:
	    pass
