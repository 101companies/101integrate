import simplejson as json
import sys

##
# converts a json file into flat representation (1 line)
def reduceJSON(infile,outfile):
  flatjson = json.dumps(json.load(open(infile,"r")))
  writer = open(outfile,"w")
  writer.write(flatjson)
  writer.close()

if __name__ == "__main__":
  reduceJSON(*sys.argv[1:])

