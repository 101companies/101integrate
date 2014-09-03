import sys
import urllib2
import json
import html2text
import os
from  BeautifulSoup import BeautifulSoup
import constants

def getChapter(url, outputfolder, ext, exElems, exClasses, exIds, posElements, posAttr):
	dom = getRefinedHtml(url, exElems, exClasses, exIds, posElements, posAttr)
	fileName = url.split('/').pop()
	f=open(outputfolder+fileName.strip(),"write")
	f.write(dom.prettify())
	f.close()

def getRefinedHtml(url, exElem, exClasses, exIds, posElements, posAttr):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	print "Downloading:", url.rstrip()
	infile = opener.open(url)
	if (infile.info()['content-type'].count('text/html') > 0):
		html = infile.read()
		print "Cleaning..."
		try:
			doc = BeautifulSoup(html)
			for exElem in exElem:
				for elem in doc.findAll(exElem):
					elem.extract()
			for exClass in exClasses:
				for d in doc.findAll(True, {'class' : exClass}):
					d.extract()
			for exId in exIds:
				for d in doc.findAll(True, {'id' : exId}):
					d.extract()
			for posElement in posElements:

				for posTag in doc.findAll(posElement, {posAttr: True}):
					posTag.insert(0, "$$$$" + posTag[posAttr] + "$$$ ")
					posTag.name = "a"

			return doc
		except ExpatError, e:
			#print "Can't extract content of " + url + " properly."
			print e

def crawl(book, perbookFldr):
    resInfos = json.loads(open(constants.configPath, 'rb').read())[book]
    for url in open((perbookFldr + book + "/metadata/chapters.txt").replace("/",os.path.sep)).readlines():
	if not url.strip(" ").strip("\r").strip("\n"):#skip empty lines
	  continue
	try:
	  exIds =  resInfos['exclude-ids']
	except  KeyError:
	  exIds = []
	else:
	  pass
	getChapter(url.rstrip(),(perbookFldr + book + "/contents/").replace("/",os.path.sep) , resInfos['ext'], resInfos['exclude-elements'], resInfos['exclude-classes'], exIds, resInfos['posElements'], resInfos['posAttr'])


if __name__ == "__main__":
   crawl(sys.argv[1],sys.argv[2])
