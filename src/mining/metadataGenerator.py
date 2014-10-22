import sys
import urllib2
import simplejson as json
import os
import re
from BeautifulSoup import BeautifulSoup
import constants



##
# @param 	an url string
# @return 	wether the url is realtive
def isRelative(url):
     #return (not (("http://" in url) or ("https://" in url)))
     return (re.match("^http(s)?:\/\/", url) is None)


##
# @param	url 	an url string
# @param 	ext		a file extension string
# @param	baseUrl	the BaseUrl on which an absolute url depends on
# @return	wether its valid url in the book's content
#DEPRECATED replaced with acceptor
def isAccepted(url, baseUrl, ext):
    return (not ("mailto:" in url) and ((not ("http:" in url)) or baseUrl in url) and (ext in url))




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
# @return	an Array of Arrays containing the the link and its descriptionackage
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
	    
##
# @param	baseUrl		the base Url
# @param	url			the url to be cleaned
# @return	the cleanedUrl or empty string if it is not below the baseUrl
def cleanUrl(baseUrl, url):
	cleanedUrls = ""
	matchingStr = "/"
	for u in baseUrl.split("/")[3:]: # http://www.anything.com/whateverinterestsme
		if u:
			matchingStr+=u+"/"
	if re.search((("("+matchingStr+"){2}").replace("/","\/")), url) is not None:
			cleaned = baseUrl +"/"+ url.replace(baseUrl,"").replace(matchingStr,"")
			cleaned = cleaned.replace("//","/").replace(":/","://")
			cleanedUrls+=cleaned
	else:
		if re.search("\/\/((\w|-|_|\.)+\/)+\/",url) is None:
			cleanedUrls+=url
	return cleanedUrls


##
# @param	links	a collection of an Array with a link and its description
# @param	url 	The Base Url all processed Urls depend on
# @return		A list of dictionaries containing file, url and title
def generateMetadata(links, url):
  chapters = []
  print "Processing links"
  for l in links:
		print l
		temp = l[0].split("/")
		filename = temp[len(temp)-1]+".txt"
		if isRelative(l[0]):
			if(url[len(url)-1] is not "/"):
				url+="/"
			writeUrl= cleanUrl(url, url+l[0])
			if writeUrl:
				chapters.append({"file": filename ,"title": l[1], "url":writeUrl})
			else:
				print " \t rejected"
		else:
			chapters.append({"file": filename,"title": l[1], "url":l[0]})
  return chapters

##
# @param	args	the books' folders
# generates chaptersGen txt and json in the book's metadata folder
# only works if the base Url is the index url
def writeMetadata(args):
  if (len(args)<=0):
    print "No book specified. Aborting."
  else:
    bookData = json.loads(open(constants.configPath , 'rb').read())
    for arg in args:
	try:
		url = bookData[arg]['urlBase'].strip()
		links = getLinks(url, bookData[arg]['ext'])
		path = constants.getMetaPath(arg)
		constants.mkdir(path)
		chapters = generateMetadata(links, url)
		chaptersFull =  open(path+"chapterData.json","w")
		chaptersFull.write(json.dumps({"chapters": chapters}, indent="\t"))
		chaptersFull.close()
		blacklist = []
		try:
		  blacklist = json.loads(open(constants.getMetaPath(arg)+"blacklist.json" , 'rb').read())
		except IOError:
		  pass
		else:
		  print "loaded Blacklist"
		chaptersWrite = open(path+"chaptersGen.txt","w")
		for c in chapters[:]:
		    if c['url'] in [e['url'] for e in blacklist]:
			chapters.remove(c)
			print c , " blacklisted"
		    else:
			chaptersWrite.write(c['url'])
			chaptersWrite.write("\r\n")
			c.pop('url')
		chaptersWrite.close()
		chaptersWriteJSON = open(path+"chaptersGen.json","w")
		chaptersWriteJSON.write(json.dumps({"chapters": chapters}, indent="\t"))
		chaptersWriteJSON.close()
		print "Metadata generated"
	except KeyError:
		print arg + " skipped."
	else:
		pass


if __name__ == "__main__":
  writeMetadata(sys.argv[1:])
