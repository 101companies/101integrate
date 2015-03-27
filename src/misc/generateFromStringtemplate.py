#!/usr/bin/env python
# -*- coding: utf-8 -*-

import stringtemplate3 as stringtemplate
#from stringtemplate3 import StringTemplateGroup, CommonGroupLoader
import sys



def main(infile, args):
	# Use the constructor that accepts a Reader
	group = stringtemplate.StringTemplateGroup(file=(open(infile, "r")))
	#StringTemplateGroup.registerGroupLoader(CommonGroupLoader(infile,ErrorManager.getStringTemplateErrorListener()))
	#group = StringTemplateGroup.loadGroup() 
	t = group.getInstanceOf("template")
	t["args"]=args
	print str(t)

if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2:])
