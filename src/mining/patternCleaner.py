import json
import re
import logging

def rchop(thestring, ending):
  if thestring.endswith(ending):
    return thestring[:-len(ending)]
  return thestring

def lchop(thestring, ending):
  if thestring.startswith(ending):
    return thestring[len(ending):]
  return thestring

def cleanPatterns(term, patterninfo):
	result = term
	for p in patterninfo:
		if not p.has_key('mustcontain') or term.count(p['mustcontain']) != 0:
			result = {
				"prefix" : lchop(result, p['string']),
				"infix" : result.replace(p['string'], ""),
				"suffix" : rchop(result, p['string'])
			}[p['pos']]
	if term != result:
		logging.info(term, "->", result)
	return result