import os
import sys
import logging #needed for nunning the whole project in debug/info-mode
import logging.config

logging.config.fileConfig('../config/pythonLogging.conf'.replace('/',os.path.sep))
f = sys.argv[1]
if f.endswith(".txt.txt"):
	os.rename(f, f.replace(".txt.txt",".txt"))
	#print f
#elif f.endswith(".html.txt"):
	#os.rename(f, f.replace(".html.txt",".txt"))
	#print f
