import sys
import constants
import simplejson as json

def generateBlacklist(args):
	for a in args:
		blacklist =[]
		path = constants.getMetaPath(a)
		try:
			chapters = json.loads(open(path + "chapterData.json", 'rb').read())['chapters']
			usedChapters =  json.loads(open(path + "chapters.json", 'rb').read())['chapters']
			for c in chapters[:]:
				for l in open(path  + "chapters.txt").readlines():
					if c['url'] == l.replace("\r","").replace("\n",""):
						chapters.remove(c)
			for c in chapters[:]:
				for u in usedChapters:
					if c['file'] == u['file'] and c['title'] == u['title']:
						chapters.remove(c) 
			blacklist = chapters
			for b in blacklist:
				b['reason'] = ""
		except IOError, e:
			print e
			print "Could not read "+a+"-Files \r\n Try running MetadataGenerator before BlacklistGenerator"
		else:
			pass
		WriteJSON = open(path+"blacklist.json","w")
		WriteJSON.write(json.dumps(blacklist, indent="\t"))
		WriteJSON.close()

if __name__ == "__main__":
  generateBlacklist(sys.argv[1:])
