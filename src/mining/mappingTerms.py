import csv
import sys
import simplejson as json
import math
import logging
import logging.config

def loadCsvData(csvFile):
		#print(csvFile)
		reader = csv.reader(open(csvFile,"rb"), delimiter=';', quotechar='\"')
		#return [z for z in [[y for y in x if y] for x in reader if x] if z] # remove all empty values
		result = list(reader)
		if len(result[0]) == 1:
			return [x[0] for x in result]
		else:
			return result

def writeData(data, outfile):
		wikiTerms = []
		try:
			wikiTerms=loadCsvData("../../data/allbooks/wikiTerms.csv")
		except IOError, e:
			logging.info("no wikiTermsFile found")
			logging.debug(e)
		logging.info("writing data")
		f = open(outfile,"wb")
		writer = csv.writer(f)
		headers=["Kind","IndexTerm","WikiTerm","Comment"]
		writer.writerow(headers)
		writeRow(writer, data['chapter'], "CHAP", wikiTerms)
		writeRow(writer, data['popular'], "FREQ", wikiTerms)
		writeRow(writer, data['title'], "TITLE", wikiTerms)	
		f.close()

def writeRow(writer, terms, prefix, wikiTerms):
	for t in terms:
			row = [prefix,t,lookupTerm(t,wikiTerms),""]
			if row[2]:
				row[3] = "automatically assigned"
			writer.writerow(row)

def lookupTerm(term,wikiTerms):
	for t in wikiTerms:
		if term.lower() == t.lower().split(":").pop():
			logging.debug("\""+term+"\" matched \""+t+"\"")
			return t
	return ""

def selectTerms(data, popularLimit=10, chapLimit=3, minOccurence=2):
		titleTerms= data[0][3:]
		data = data[1:]
		data = [x[0:3]+[int(y) for y in x[3:]] for x in data] #convert numeric data to int 
		logging.debug("dataset:"+str(data))
		logging.info("Selecting "+popularLimit+" most common Terms")
		popularTerms = [x[0] for x in sorted(data, key=(lambda x: sum(x[3:len(data[0])])), reverse=True) if sum(x[3:len(data[0])])>=int(minOccurence)][:int(popularLimit)]
		data = [x for x in data if x[0] not in popularTerms]
		logging.debug("Popular Terms")
		logging.debug(popularTerms)
		logging.debug("applying inverse document frequency")
		data = getInverseDocumentFrequency(data)
		chapterTerms=[]
		logging.info("Selecting "+chapLimit+" most important Terms per chapter")
		for i in range(3,len(data[0])):
				logging.debug("processing chapter "+str(i-2))
				logging.debug([[x[0],x[i]] for x in data])
				chapterTerms=chapterTerms + sorted([x[0] for x in sorted(data, key=(lambda x: x[i][1]),reverse=True) if x[i][0]>=int(minOccurence)][:int(chapLimit)])
				data = [x for x in data if x[0] not in chapterTerms]
		logging.debug("chapterTerms")
		logging.debug(chapterTerms)
		return {"chapter":chapterTerms,"popular":sorted(popularTerms),"title":titleTerms}

def getInverseDocumentFrequency(data):
	data = [x[:3]+[[y,0] for y in x[3:]] for x in data]
	data = [x[:3]+[[y[0],(y[0]*math.log10((len(x)-3)/len([y for y in x[3:] if y[0]])))] if y[0] else y for y in x[3:]] for x in data]
	return data
	
def main(datafldr,csvFile,outFile,popularLimit=10,chaplimit=3,minOccurence=2):
		data = loadCsvData(datafldr+csvFile)
		#print data
		results= selectTerms(data,popularLimit,chaplimit,minOccurence)
		#print results
		writeData(results, datafldr+outFile)

if __name__ == "__main__":
	logging.config.fileConfig('../config/pythonLogging.conf')
	main(*sys.argv[1:])

