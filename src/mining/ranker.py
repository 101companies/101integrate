import urllib
from string import Template
import csv

index = csv.reader(open(' ../../data/allbooks/Index.csv', 'rb'), delimiter=' ', quotechar='|')
for row in index:
	for el in row:
		#print el
		req = Template('http://www.wordcount.org/dbquery.php?toFind=$term&method=SEARCH_BY_NAME')
		f = urllib.urlopen(req.substitute(term=el))
		s = f.read() # expected result: &wordFound=yes&totalWords=86799&rankOfRequested=31
		f.close()

		res = s.split('&');
		#print res
		if res[1] == "wordFound=yes":
			#print "FOUND"
			rank = res[3].replace("rankOfRequested=", '') #rankOfRequested=31
			print el + ";" + rank
		#else : print "NOT FOUND"
