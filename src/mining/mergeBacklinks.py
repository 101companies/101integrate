#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import simplejson as json
import logging
import logging.config

def main(datafolder,origin, resNames, destination):
	logging.info(str(resNames))
	allBacklinks = {"resources" : {}, "backlinks": {}}
	resInfos = json.loads(open("../config/config.json", 'rb').read())
	for resName in resNames:
		allBacklinks['resources'][resName] = {'fullName' : resInfos[resName]['fullName'], 'isLinkable': resInfos[resName]['isLinkable']}
		resources = json.load(open(datafolder + origin  + resName + "/backlinks.json", "read"))
		for term in resources:
			if term in allBacklinks['backlinks']:
				allBacklinks['backlinks'][str(term)][resName] = resources[term]
			else:
				allBacklinks['backlinks'][str(term)] = {resName: resources[term]}

	f = open(datafolder + destination + "backlinks.json", 'write')
	f.write(json.dumps(allBacklinks, indent="\t"))

if __name__ == "__main__":
	logging.config.fileConfig('../config/pythonLogging.conf')
	main(sys.argv[1],sys.argv[2],sys.argv[3:-1],sys.argv[-1])
