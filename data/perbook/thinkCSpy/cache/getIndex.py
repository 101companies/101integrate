import urllib2
from  BeautifulSoup import BeautifulSoup
import html2text
import re

def normalizeWord(word):
	return re.sub("[^\w]", "", word.lower()).strip()

def notXmlTag(word):
	return bool(re.sub("<(.)*>", "", word).strip())

def main():
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	infile = opener.open("http://www.greenteapress.com/thinkpython/thinkCSpy/html/dex.html")
	if (infile.info()['content-type'].count('text/html') > 0):
			doc = BeautifulSoup(infile.read())
			#print(doc)
			#print(type())
                        for a in doc.findAll('a'): #removing references	
                                        a.extract() 
			doc = doc.findAll('td')[0].findAll('td')[:2]
			output = ""
			for d in doc:
				output += d.prettify()
				output += "<br/>\r\n"
			print output
			output = output.replace("<br />","\r\n").replace("&nbsp; &nbsp; &nbsp;","\t")
			terms = []
			for o in output.splitlines(True):
				if normalizeWord(o) and notXmlTag(o):
					if "\t" in o.rstrip():
						terms.append([o.strip().split("...")[0],True])
						print o
						print terms[-1]
					else:
						terms.append([o.strip().split("...")[0],False])
						print o
						print terms[-1]
			#print terms
			writer = open("index.txt", "w")
			for t in terms:
				if t[1]:
					writer.write("\t"+t[0]+"\r\n")
				else:
					writer.write(t[0]+"\r\n")
			writer.close()


if __name__ == "__main__":
	main()
