import os
import sys

f = sys.argv[1]
if f.endswith(".txt.txt"):
	os.rename(f, f.replace(".txt.txt",".txt"))
	#print f
elif f.endswith(".html.txt"):
	os.rename(f, f.replace(".html.txt",".txt"))
	#print f
