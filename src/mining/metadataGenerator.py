##
# @param	systemargs	the books' folders
# generates chaptersGen txt and json in the book's metadata folder
# only works if the base Url is the index url

import sys
import urllib2
import simplejson as json
import os
import re
from BeautifulSoup import BeautifulSoup


# the path for the data folder
dataPath = ".."+os.path.sep+".."+os.path.sep+"data"


##
# @param 	a string with the books folder
# @return 	the relative path to the book's metadata folder
# creates the path if it does not exist
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




##
# @param 	an url string
# @return 	wether the url is realtive
def isRelative(url):
     #return (not (("http://" in url) or ("https://" in url)))
     return (re.match("^http(s)?:\/\/", url) is None)


##
# @param	url 	an url string
# @url 		ext	a file extension string
# @return	wether its valid url in the book's content
#DEPRECATED replaced with acceptor
def isAccepted(url, ext):
    return (not ("mailto:" in url) and ((not ("http:" in url)) or url in url) and (ext in url))




##
# @param	urlBase		book's base url string
# @param	ext		file extension string
# @return	an re-object for accepting valid book urls
def createAcceptor(urlBase, ext):
    regex=""
    for url in urlBase.split("/"):
	regex ="("+regex+"("+url+"/))?"
    regex += "((-|\w)*(/)?){1,3}"+ext+"($|\Z)" #\Z and $ indicates end of String
    regex= "^(\/)?"+ regex.replace("/","\/").replace(".","\.") # escaping chars  ; ^indicates beginning of string
    return re.compile(regex)


##
# @param	url 	the url which links are to be extracted
# @param	ext 	the file extension for the extracted links
# @return	an Array of Arrays containing the the link and its description
def getLinks(url,ext):
	    opener = urllib2.build_opener()
	    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	    links = []
    	    print "creating url Acceptor"
	    acceptor = createAcceptor(url, ext)
	    print "Regex-Term:"+acceptor.pattern
	    print "checking " + url
	    infile = opener.open(url)
	    if (infile.info()['content-type'].count('text/html') > 0):
		  doc = BeautifulSoup(infile.read())
		  for l in doc.findAll('a'):
		      info = [ l.get('href'), l.string]
		      if info[0] is not None and info[1] is not None:
			  if acceptor.match(info[0]) is not None:
			      links.append(info)
	    print "collected Information"
	    opener.close()
	    return links



if (len(sys.argv)<=1):
    print "No book specified. Aborting."
else:
    bookData = json.loads(open("config"+os.path.sep+"config.json", 'rb').read())
    for arg in sys.argv[1:]:# skipping 0 
	try:
		url = bookData[arg]['urlBase'].strip()
		links = getLinks(url, bookData[arg]['ext'])
		path = getMetaPath(arg)
		chaptersWrite = open(path+"chaptersGen.txt","w")
		chapters = []
		print "Processing links"
		for l in links:
			print l
			if isRelative(l[0]):
				if(url[len(url)-1] is not "/"):
					url+="/"
				chaptersWrite.write(url+l[0])
				filename = l[0]+".txt"
				filename = filename.split("/")
				filename = filename[len(filename)-1]
				chapters.append({"file": filename ,"title": l[1], "url": (url+l[0])})
			else:
				temp = l[0].split(os.path.sep)
				filename = temp[len(temp)-1]+".txt"
				chapters.append({"file": filename,"title": l[1]})
				chaptersWrite.write(l[0])
			chaptersWrite.write("\r\n")
		chaptersWrite.close()
		chaptersWriteJSON = open(path+"chaptersGen.json","w")
		chaptersWriteJSON.write(json.dumps({"chapters": chapters}, indent="\t"))
		chaptersWriteJSON.close()
		print "Metadata generated"
		cleanedUrls = ""
		matchingStr = "/"
		for u in url.split("/")[3:]: # http://www.anything.com/whateverinterestsme
			if u:
				matchingStr+=u+"/"
		finder = re.compile("("+matchingStr+"){2}")
		for line in open((path+"chaptersGen.txt")).readlines():
			if finder.search(line) is not None:
					cleaned = url +"/"+ line.replace(url,"").replace(matchingStr,"")
					cleaned = cleaned.replace("//","/").replace(":/","://")
					cleanedUrls+=cleaned
			else:
					cleanedUrls+=line
			cleanedUrls  + "\r\n"
		chaptersWrite = open(path+"chaptersGen.txt","w")
		chaptersWrite.write(cleanedUrls)
		chaptersWrite.close()
		print "urls cleaned"
	except KeyError:
		print arg + " skipped."
	else:
		pass
