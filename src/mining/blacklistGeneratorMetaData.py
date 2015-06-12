import sys
import constants
import simplejson as json
import logging #needed for nunning the whole project in debug/info-mode
import logging.config

def generateBlacklist(args):
	for a in args:
		blacklist =[]
		path = constants.getMetaPath(a)
		try:
		    blacklist = json.loads(open(path+"blacklist.json" , 'rb').read())
		except IOError:
		    pass
		else:
		    print "loaded old blacklist"
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
			newBlacklist = chapters
			print "generated Blacklist"
			for b in newBlacklist:
				b['reason'] = ""
			# Keep reasons
			if blacklist:
			    print "copying reasons"
			for b in blacklist:
			    for n in newBlacklist:
				if b['url'] == n['url'] and b['title'] == n['title']:
				    n['reason']=b['reason']
			blacklist = newBlacklist
		except IOError, e:
			print e
			print "Could not read "+a+"-Files \r\n Try running MetadataGenerator before BlacklistGenerator"
		else:
			pass
		WriteJSON = open(path+"blacklist.json","w")
		WriteJSON.write(json.dumps(blacklist, indent="\t"))
		WriteJSON.close()
		print "Wrote File"

if __name__ == "__main__":
	logging.config.fileConfig('../config/pythonLogging.conf'.replace('/',os.path.sep))
	generateBlacklist(sys.argv[1:])
