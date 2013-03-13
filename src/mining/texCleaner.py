import sys
import re
import os
import json

rid = sys.argv[1]
config = json.loads(open("config/config.json").read())[rid]
root = sys.argv[2]
realcnamesraw = json.loads(open(root + "/metadata/chapters.json", 'rb').read())['chapters']
realcnames = {}
for i,x in enumerate(realcnamesraw):
	realcnames[realcnamesraw[i]['file']] = realcnamesraw[i]['title']
texFileNames = filter(lambda x: x.endswith(".tex") and x in realcnames, os.listdir(root + "/contents/"))
for texFileName in texFileNames:
	print texFileName + ":"
	f = open(path + "/data/" + texFileName, "r")
	tex = f.read()
	envs = config['exclude-env']
	result = tex
	for env in envs:
		tempr = result
		result = result.split("\\begin{" + env + "}",-1)[0]
		print "\tDealing with", env
		for m in tempr.split("\\begin{" + env + "}",-1)[1:]:
			result += m.split("\\end{" + env + "}",-1)[1]
	print "\tdeleted characters:", len(tex)-len(result)
	f2 = open(path + "/data/clean/" + texFileName, "w")
	f2.write(result)
	f2.close()
	f.close()
