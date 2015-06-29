import sys
import urllib2
import simplejson as json
import os
import re
from BeautifulSoup import BeautifulSoup
import constants
import itertools
import logging #needed for nunning the whole project in debug/info-mode


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
	for i, url in enumerate(urlBase.split("/")):
		if url or i <= 2:
			regex ="("+regex+"("+url+"/))?"
	regex += "((_|-|\w)*(/)?){1,3}"+ext+"($|\Z)" #\Z and $ indicates end of String
	regex= "^(\/)?"+ regex.replace("/","\/").replace(".","\.") # escaping chars  ; ^indicates beginning of string
	return re.compile(regex)


##
# @param	tocurl 	the url which links are to be extracted
# @param	baseurl	the url all links have to derive from
# @param	ext 	the file extension for the extracted links
# @return	an Array of Arrays containing the the link and its description
def getLinks(baseurl,tocurl,ext):
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		links = []
		print "creating url Acceptor"
		acceptor = createAcceptor(baseurl, ext)
		print "Regex-Term:"+acceptor.pattern
		print "checking " + tocurl
		infile = opener.open(tocurl)
		if (infile.info()['content-type'].count('text/html') > 0):
			doc = BeautifulSoup(infile.read())
			for l in doc.findAll('body')[0].findAll('a'):
				info = [ l.get('href'), l.string, l.get('title')]
				info = [i.strip() for i in info if i is not None]
				#print info
				if len(info) >=2:
					if acceptor.match(info[0]) is not None:
						#print "\t\t accepted "+str(info)
						if info[0] in [x[0] for x in links]:
							temp = [x for x in links if x[0] == info[0]][0]
							links.remove(temp)
							temp.append(info[1])
							links.append(temp)
						else:
							links.append(info)
		print "collected Information"
		opener.close()
		return links
		#links = sorted(links)
		#return [links[i] for i in range(len(links)) if i == 0 or links[i] != links[i-1]] #remove duplicates
	    
##
# @param	baseUrl		the base Url
# @param	url			the url to be cleaned
# @return	the cleanedUrl or empty string if it is not below the baseUrl
def cleanUrl(baseUrl, url):
	if url.endswith("/"): url = url[0:-1]
	cleanedUrls = ""
	matchingStr = "/"
	for u in baseUrl.split("/")[3:]: # http://www.anything.com/whateverinterestsme
		if u:
			matchingStr+=u+"/"
	if re.search((("("+matchingStr+"){2}").replace("/","\/")), url) is not None:
			cleaned = baseUrl +"/"+ url.replace(baseUrl,"").replace(matchingStr,"")
			cleaned = cleaned.replace("//","/").replace(":/","://")
			cleanedUrls+=cleaned
	elif (re.search("\/\/((\w|-|_|\.)+\/)+\/",url) is None) and (baseUrl in url):
			cleanedUrls+=url
        return cleanedUrls


##
# @param		links			a collection of an Array with a link and its description
# @param		url 			The Base Url all processed Urls depend on
# @param		onlyFirstTitle	wether only one of the possible Titles shoud be retrieved
# @return		A list of dictionaries containing file, url and title
def generateMetadata(links, url, useFullPath=False, onlyFirstTitle=False):
	chapters = []
	print "Processing links"
	for l in links:
		print "\t"+str(l)
		filename =  "" #Getting Filename
		if useFullPath:
			filename = re.sub("((\.)+)|((\/)+)", ".", l[0].replace(url,"")+".txt")
		elif (l[0].split("/"))[-1]:
			filename = (l[0].split("/"))[-1]+".txt"
			if filename.startswith("index."):
				filename = (l[0].split("/"))[-2] + "." + filename
		else:
			filename = (l[0].split("/"))[-2]+".txt" # if link refers to "invisible" index.html
		if isRelative(l[0]):
			if not (url[-1] == "/"):
				url+="/"
			writeUrl = cleanUrl(url, url+l[0])
			if writeUrl:
				chapters.append({"file": filename ,"title": l[1:], "url":writeUrl})
				#print "\t\t"+str(chapters[-1])
			else:
				print "\t \t rejected"
		else:
			chapters.append({"file": filename,"title": l[1:], "url":l[0]})
	if onlyFirstTitle:
		for c in chapters: c['title']=c['title'][0]
	return chapters

##
# @param	book			the book's folder
# @param	onlyFirstTitle	wether only one of the possible Titles shoud be written into the generated File
# generates chaptersGen txt and json in the book's metadata folder
# only works if the base Url is the index url
def writeMetadata(book, onlyFirstTitle=False):
	bookData = json.loads(open(constants.configPath , 'rb').read())
	try:
		url = bookData[book]['urlBase'].strip() # baseurl
		tocurl="" # Table of contents url
		try:
			tocurl = bookData[book]['tocUrl'].strip()
		except KeyError:
			tocurl=url
		links = getLinks(url,tocurl, bookData[book]['ext'])
		path = constants.getMetaPath(book)
		constants.mkdir(path)
		#print links
		chapters=[]
		try:
			chapters = generateMetadata(links, url,bookData[book]['useFullPathAsFilename'],bool(onlyFirstTitle))
		except KeyError:
			chapters = generateMetadata(links, url, False, bool(onlyFirstTitle))
		chaptersFull =  open(path+"chapterData.json","w")
		chaptersFull.write(json.dumps({"chapters": chapters}, indent="\t"))
		chaptersFull.close()
		blacklist = []
		try:
			blacklist = json.loads(open(constants.getMetaPath(book)+"blacklist.json" , 'rb').read())
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
				if len(c['title']) is 1:
					c['title']=c['title'][0]
		chaptersWrite.close()
		chaptersWriteJSON = open(path+"chaptersGen.json","w")
		chaptersWriteJSON.write(json.dumps({"chapters": chapters}, indent="\t"))
		chaptersWriteJSON.close()
		print "Metadata generated"
	except KeyError:
		print book + " skipped."
	else:
		pass


if __name__ == "__main__":
	if (len(sys.argv)==1):
		print "No book specified. Aborting."
	else:
		writeMetadata(*sys.argv[1:])
