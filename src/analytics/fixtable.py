import glob
import os
os.chdir("./")
for fileName in glob.glob("*.tex"):
	f = open(fileName, "r")
	text = f.read()
	f.close()
	#print text
	replaced = text.replace("[ht]", "[ht]");
	#print replaced	
	print fileName
	f1 = open(fileName, "w")
	f1.write(replaced) # Write a string to a file
	f1.close()
