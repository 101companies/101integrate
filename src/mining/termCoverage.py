import sys
import urllib
import urllib2
import json
import wikitools as wiki

apiurl = 'http://101companies.org/api.php'
wiki101 = wiki.Wiki(apiurl)

def getHaskellContribs(lang):
  host = 'http://sl-mac.uni-koblenz.de'
  port = '8081'
  service = 'org.softlang.semanticendpoint/doQuery'
  parameters = {'method' : 'getResourceTriples', 'resource' : 'Language-3A' + lang}
  url = '%s:%s/%s?%s' % (host, port, service, urllib.urlencode(parameters))
  triples = json.loads(urllib2.urlopen(url).read().replace('callback(','').replace(')',''))
  contribTriples = filter(lambda t : t['predicate'] == 'http://101companies.org/property/uses', triples)
  return map(lambda t : t['node'].replace('-3A','/').split('/')[-1], contribTriples)

resourcebase = sys.argv[1]

mappedTerms = set([])
mapping = json.loads(open(resourcebase + 'mapping.json', 'rb').read())
for resource in mapping:
	mappedTerms |= set(mapping[resource].keys())
for term in sorted(mappedTerms):
	print term
raw_input();

level0Links = {}
level1Links = {}
result = '<table align=middle style="border: 0.5px solid black; border-spacing: 0px;">'
result += '<tr style="height:140px;"><th style="border: 1px solid black; -webkit-transform:">Contribution/Term</th>'
contribs = set((getHaskellContribs('Haskell')  + getHaskellContribs('Haskell_98')))
for contribName in sorted(contribs):
	result += '<th style="border: 1px solid black; vertical-align:top; padding-top: 3px;"><span align="right" style="display: inline-block; width: 22px;white-space: nowrap; -webkit-transform: rotate(90deg);">' + contribName + '</span></th>'''
	print 'Checking', contribName, '...'
	print ' Finding level 0 links ...'
	page = wiki.Page(title='Contribution:'+contribName, site=wiki101)
	clevel0Links = page.getLinks()
	level0Links[contribName] = clevel0Links
	clevel1Links = []
	print '', str(len(clevel0Links)), 'level 0 links found.'
	#print clevel0Links
	#raw_input()
	print ' Finding level 1 ...'
	for link in clevel0Links:
		linkPage = wiki.Page(title=link, site=wiki101)
		try:
			for deeplink in linkPage.getLinks():
				try:
					clevel1Links.append(deeplink)
				except Exception:
					pass
		except Exception:
			pass
	level1Links[contribName] = clevel1Links
	print '', str(len(clevel1Links)), 'level 1 links found.'
result += '<th style="border: 1px solid black;">' + str(len(contribs)) + '</th></tr>'


for term in sorted(mappedTerms):
	result += '<tr><td  style="border: 1px solid black;"><b>' + term + '</b></td>'
	level0 = 0
	level1 = 0
	for contribName in sorted(contribs):
		result += '<td  align=middle style="border: 1px solid black";>'
		if term in level0Links[contribName]:
			level0 += 1
			result += '&#8855;'
		elif term in level1Links[contribName]:
			level1 += 1
			result += '&#8226;'
		result +=  '</td>'
	result += '<td  align=middle style="border: 1px solid black";>' + str(level0) + ' (' + str(level1) + ')</td>'
	result += '<tr>'
result += '<tr><td style="border: 1px solid black";><b>Total</b></td>'
for contribName in sorted(contribs):
	mappedLevel0 = filter(lambda x: x in mappedTerms, level0Links[contribName])
	mappedLevel1 = filter(lambda x: x in mappedTerms, level1Links[contribName])
	result += '<td align=middle style="border: 1px solid black";>' + str(len(mappedLevel0)) + '<br>(' + str(len(mappedLevel1)) + ')</td>'
result += '<td></td></tr>'
result += '</table>'

with open(resourcebase + 'coverage.html', 'write') as tablef:
	tablef.write(result)

