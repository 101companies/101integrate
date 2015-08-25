#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import simplejson as json
import csv
import logging
import logging.config

def main(datafolder, origin, resNames, destination):
	logging.info("Checking..." + str(resNames))
	mappings = {}
	for resName in resNames:
		rawmapping = csv.reader(open(datafolder + origin  + resName + "/metadata/mapping.csv"), delimiter=',')
		mapping = {}
		for row in rawmapping:
			if len(row) >=3:
				if row[0] != 'Kind' and row[2]:
					mapping[row[2]] = row[1]
		mappings[resName] = mapping

	f = open(datafolder + destination + "mapping.json", 'write')
	f.write(json.dumps(mappings,indent="\t"))

if __name__ == "__main__":
	logging.config.fileConfig('../config/pythonLogging.conf')
	main(sys.argv[1],sys.argv[2],sys.argv[3:-1],sys.argv[-1])
