import sys
import csv
import simplejson as json

def readFile(file):
    content = []
    with open(file, "rb") as csvfile:
	for row in csv.reader(csvfile, delimiter=";", quotechar="\""):
	  content.append(row)
    return content



def getDiff(file1,file2):
  f1 = readFile(file1)
  f2 = readFile(file2)
  deletions = []
  for l in f1:
    if l not in f2:
      deletions.append(l)
  additions = []
  for l in f2:
    if l not in f1:
      additions.append(l)
  if f1[0] is f2[0] and len(f1[0])>1:
    return {"del":deletions, "add":additions, "columnHeader":f1[0]}
  else:
    return {"del":deletions, "add":additions}



def transformToJSON(dic):
  newdic = []
  for key in dic:
    for e in dic[key]:
	newdic.append({"value":e,"type":key,"reason":""})
  return newdic



def transformToCSV(dic):
  newdic= []
  temp = dic.keys()
  if ("columnHeader" in temp):
    newdic.append(dic["columnHeader"]+["Type","Reason"])
    temp.remove("columnHeader")
  else:
    newdic.append(["Value","Type","Reason"])
  for key in temp:
    for e in dic[key]:
      newdic.append(e+[key,""])
  return newdic



def writeCsv(dic, outFile):
  with open(outFile, "wb") as csvfile:
      writer = csv.writer(csvfile, delimiter=";", quotechar="\"")
      for l in dic:
	writer.writerow(l)




def writeJSON(dic, outFile):
  writer = open(outFile, "w")
  writer.write(json.dumps(dic, indent="\t"))
  writer.close()




def main(file1, file2, outSel="", outFormat="", outFile=""):
  #print [file1, file2, outSel, outFormat, outFile]
  diffs = getDiff(file1, file2)
  if outSel:
    diffs = {outSel:diffs[outSel]}
  if ((not outFormat) and (not outFile)):
    print diffs
  else:
      if outFormat.lower() == "json":
	writeJSON(transformToJSON(diffs), outFile)
      elif outFormat.lower() == "csv":
	writeCsv(transformToCSV(diffs), outFile)
      else:
	print "Unknown output type: " + outFormat



if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "too few arguments \n exiting."
  elif len(sys.argv) is 5:
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],"diff."+sys.argv[4].lower())
  else len(sys.argv):
    main(*sys.argv[1:])
    
  
