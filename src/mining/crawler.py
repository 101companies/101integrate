import sys
import urllib2
import json
import html2text
from BeautifulSoup import BeautifulSoup

def getChapter(url, outputfolder, ext, exElems, exClasses, posElements, posAttr):
	dom = getRefinedHtml(url, exElems, exClasses, posElements, posAttr)
	fileName = url.split('/').pop()
	f=open(outputfolder+fileName.strip(),"write")
	f.write(dom.prettify())
	f.close()

def getRefinedHtml(url, exElem, exClasses, posElements, posAttr):
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
			for posElement in posElements:

				for posTag in doc.findAll(posElement, {posAttr: True}):
					posTag.insert(0, "$$$$" + posTag[posAttr] + "$$$ ")
					posTag.name = "a"

			return doc
		except ExpatError, e:
			#print "Can't extract content of " + url + " properly."
			print e

resInfos = json.loads(open("config/config.json", 'rb').read())[sys.argv[1]]
for url in open(sys.argv[2] + sys.argv[1] + "/metadata/chapters.txt").readlines():
	getChapter(url.rstrip(), sys.argv[2] + sys.argv[1] + "/contents/" , resInfos['ext'], resInfos['exclude-elements'], resInfos['exclude-classes'], resInfos['posElements'], resInfos['posAttr'])
