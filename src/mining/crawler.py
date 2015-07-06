import sys
import urllib2
import json
import html2text
import os
from  BeautifulSoup import BeautifulSoup
import constants
import logging
import logging.config
import re




def getChapter(url, outputfolder, ext, exElems, exClasses, exIds, posElements, posAttr, useFullPath, baseUrl):
	dom = getRefinedHtml(url, exElems, exClasses, exIds, posElements, posAttr)
	fileName = url.split('/').pop()
	if not fileName:
		fileName = url.split('/')[-2]
	elif fileName.startswith("index."):
		fileName = ".".join(url.split('/')[-2:])
	elif useFullPath:
		logging.debug("using Full Path")
		fileName = url.replace(baseUrl,"").replace("/",".")
	#logging.debug(fileName)
	fileName = fileName.strip()+".txt"
	logging.debug("Writing "+fileName)
	f=open(outputfolder+fileName,"write")
	f.write(dom.prettify())
	f.close()
	logging.debug("Finished writing")

def getRefinedHtml(url, exElem, exClasses, exIds, posElements, posAttr):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	logging.info("Downloading:"+ url.rstrip())
	infile = opener.open(url)
	if (infile.info()['content-type'].count('text/html') > 0):
		html = infile.read()
		logging.info("Cleaning...")
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
	exIds=[]
	try:
	  exIds =  resInfos['exclude-ids']
	except  KeyError:
	  exIds = []
	useFullPath = False
	try:
	  useFullPath =  resInfos['useFullPathAsFilename']
	except  KeyError:
	  useFullPath = False
	getChapter(url.rstrip(),(perbookFldr + book + "/contents/").replace("/",os.path.sep) , resInfos['ext'], resInfos['exclude-elements'], resInfos['exclude-classes'], exIds, resInfos['posElements'], resInfos['posAttr'],useFullPath, resInfos['urlBase'])


if __name__ == "__main__":
	logging.config.fileConfig('../config/pythonLogging.conf'.replace('/',os.path.sep))
	crawl(sys.argv[1],sys.argv[2])
