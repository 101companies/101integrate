import urllib
from string import Template
import csv
import sys
import re
import logging
import logging.config

def normalizeWord(word):
  return re.sub("[^\w\-\_\.\+']", "", word).strip()


def getRankFromWordnet(word):
    req = Template('http://www.wordcount.org/dbquery.php?toFind=$term&method=SEARCH_BY_NAME')
    f = urllib.urlopen(req.substitute(term=word))
    s = f.read() # expected result: &wordFound=yes&totalWords=86799&rankOfRequested=31
    f.close()
    res = s.split('&');
    logging.debug(res)
    if res[1] == "wordFound=yes":
	logging.debug("FOUND")
	rank = res[3].replace("rankOfRequested=", '') #rankOfRequested=31
	logging.info( word + ";" + rank)
	return int(rank)
    else : 
	logging.debug("NOT FOUND")
	return False

def main(directory, infile, resource,  outfile):
    index = []
    for r in resource:
	index = index + list(csv.reader(open(directory+r+infile, 'rb'), delimiter=' ', quotechar='|'))
    logging.info("Read indices")
    used = []
    result = []
    for row in index:
	    for el in row:
	      el = normalizeWord(el)
	      if (not el in used) and el: 
		    logging.debug(el)
		    rank = getRankFromWordnet(el)
		    if rank:
			result.append([el, rank])
		    used.append(el)
    logging.debug("sorting results")
    result.sort(key=lambda x: x[1])
    logging.info("writing results to" + outfile)
    writer = csv.writer(open(outfile, "wb"))
    writer.writerows(result)

if __name__ == "__main__":
	logging.config.fileConfig('../config/pythonLogging.conf')
	main(sys.argv[1],sys.argv[2],sys.argv[3:-1],sys.argv[-1])
