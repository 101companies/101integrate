import sys
import constants
import simplejson as json

def generateBlacklist(args):
	for a in args:
		try:
			path = constants.getMetaPath(a)
			chapters = json.loads(open(path + "chapterData.json", 'rb').read())
			usedChapters =  json.loads(open(path + "chapters.json", 'rb').read())
			print path
		except IOError, e:
			print e
			print "Could not read "+a+"-Files \r\n Try running MetadataGenerator before BlacklistGenerator"
		else:
			pass

if __name__ == "__main__":
  generateBlacklist(sys.argv[1:])
