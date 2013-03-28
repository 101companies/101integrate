#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json

resNames = sys.argv[3:-1]
print resNames
datafolder = sys.argv[1]
allBacklinks = {"resources" : {}, "backlinks": {}}
resInfos = json.loads(open("config/config.json", 'rb').read())
for resName in resNames:
	allBacklinks['resources'][resName] = {'fullName' : resInfos[resName]['fullName'], 'isLinkable': resInfos[resName]['isLinkable']}
	resources = json.load(open(datafolder + sys.argv[2]  + resName + "/backlinks.json", "read"))
	for term in resources:
		if term in allBacklinks['backlinks']:
			allBacklinks['backlinks'][str(term)][resName] = resources[term]
		else:
			allBacklinks['backlinks'][str(term)] = {resName: resources[term]}

f = open(datafolder + sys.argv[-1] + "backlinks.json", 'write')
f.write(json.dumps(allBacklinks))
