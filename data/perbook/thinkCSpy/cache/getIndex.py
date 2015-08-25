import urllib2
from  BeautifulSoup import BeautifulSoup
import html2text
import re

def normalizeWord(word):
  return re.sub("[^\w]", "", word.lower()).strip()

def main():
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	infile = opener.open("http://www.greenteapress.com/thinkpython/thinkCSpy/html/dex.html")
	if (infile.info()['content-type'].count('text/html') > 0):
			doc = BeautifulSoup(infile.read())
			#print(doc)
			#print(type())
			doc = doc.findAll('td')[0].findAll('td')[0].findAll('font')[0]
			for a in doc.findAll('a'):
					a.extract()
			output = doc.prettify()
			output = output.replace("<br />","\r\n").replace("&nbsp; &nbsp; &nbsp;","\t")
			terms = []
			for o in output.splitlines(True):
				if normalizeWord(o):
					if o.startswith("\t"):
						terms.append(("\t"+o.strip()).split("...")[0])
					else:
						terms.append(o.strip().split("...")[0])
			writer = open("index.txt", "w")
			writer.write("\r\n".join(terms))
			writer.close()


if __name__ == "__main__":
	main()
