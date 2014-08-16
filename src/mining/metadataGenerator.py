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
			cleanedUrls+=line
	return cleanedUrls


##
# @param	args	the books' folders
# generates chaptersGen txt and json in the book's metadata folder
# only works if the base Url is the index url
def generateMetadata(args):
  if (len(args)<=0):
    print "No book specified. Aborting."
  else:
    bookData = json.loads(open(constants.configPath , 'rb').read())
    for arg in args:
	try:
		url = bookData[arg]['urlBase'].strip()
		links = getLinks(url, bookData[arg]['ext'])
		path = constants.getMetaPath(arg)
		chaptersWrite = open(path+"chaptersGen.txt","w")
		chapters = []
		print "Processing links"
		for l in links:
			print l
			if isRelative(l[0]):
				if(url[len(url)-1] is not "/"):
					url+="/"
				writeUrl= cleanUrl(url, url+l[0])
				if writeUrl:
						chaptersWrite.write(writeUrl)
						filename = l[0]+".txt"
						filename = filename.split("/")
						filename = filename[len(filename)-1]
						chapters.append({"file": filename ,"title": l[1], "url":writeUrl})
				else:
					print " \t rejected"
			else:
				temp = l[0].split(os.path.sep)
				filename = temp[len(temp)-1]+".txt"
				chapters.append({"file": filename,"title": l[1], "url":l[0]})
				chaptersWrite.write(l[0])
			chaptersWrite.write("\r\n")
		chaptersWrite.close()
		chaptersFull =  open(path+"chapterData.json","w")
		chaptersFull.write(json.dumps({"chapters": chapters}, indent="\t"))
		chaptersFull.close()
		for c in chapters:
			c.pop('url')
		chaptersWriteJSON = open(path+"chaptersGen.json","w")
		chaptersWriteJSON.write(json.dumps({"chapters": chapters}, indent="\t"))
		chaptersWriteJSON.close()
		print "Metadata generated"
	except KeyError:
		print arg + " skipped."
	else:
		pass


if __name__ == "__main__":
  generateMetadata(sys.argv[1:])
