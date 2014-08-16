import nltk
import sqlite3 as sqlite
import os
import sys
import re

# the path for the data folder
dataPath = ".."+os.path.sep+".."+os.path.sep+"data"




##
# @param 	a string with the books folder
# @return 	the relative path to the book's content folder
def getContentPath(book):
    return getPath(book)+"contents"+os.path.sep
  
  
  
  
##
# @param 	a string with the books folder
# @return 	the relative path to the book's folder
def getPath(book):
    return dataPath+os.path.sep+"perbook"+os.path.sep+book+os.path.sep





def sqlExec(cursor, statement, values):
  try:
	cursor.execute(statement, values)
  except sqlite.IntegrityError, e:
	print e
  else:
	pass  
      



def transformParagraphToLine(path):
    temp = ""
    for l in open(path).readlines():
	  if not l.replace(" ","").replace("\t","").replace("\r","").replace("\n",""):
	      temp +="\r\n \r\n"
	  else:
	      temp += l.replace("\r","").replace("\n","")
    writer = open(path, "w")
    writer.write(temp)
    writer.close




def main(args):
    for a in args:
	conPath = getContentPath(a)
	files = os.listdir(conPath)
	sqlcon = sqlite.connect(getPath(a)+"Entries.db")
	sqlcon.text_factory = str
	cursor = sqlcon.cursor()
	print "connected to DB"
	cursor.execute(""" CREATE TABLE IF NOT EXISTS words ( word TEXT , tag TEXT, file TEXT, frequency INTEGER)""")
	cursor.execute(""" CREATE TABLE IF NOT EXISTS files(file TEXT PRIMARY KEY)""")
	cursor.execute(""" CREATE TABLE IF NOT EXISTS links(w1 TEXT, tag1 TEXT, w2 TEXT, tag2 TEXT, file TEXT, frequency INTEGER)""")
	#cursor.execute(""" CREATE TABLE IF NOT EXISTS wordorder(n1 INTEGER, n2 INTEGER, file TEXT, frequency INTEGER)""")
	cursor.execute(""" CREATE VIEW IF NOT EXISTS linkstotal as SELECT w1, w2, tag1, tag2, SUM(frequency) as freq FROM links GROUP BY w1, w2, tag1, tag2""")
	cursor.execute(""" CREATE VIEW IF NOT EXISTS wordstotal as SELECT word, tag, SUM(frequency) as freq FROM words GROUP BY word, tag""")
	fileStm = """INSERT INTO files(file) VALUES(:file)  """
	wordStm = """INSERT INTO words(word, tag, file, frequency) VALUES(:word, :tag, :file , 0 )"""
	linksStm = """ INSERT INTO links(w1,tag1, w2, tag2, file, frequency) VALUES(:w1 , :tag1 , :w2 , :tag2 , :file , 0) """
	wordIncStm = """ UPDATE words SET frequency=frequency+1 WHERE word = :word AND tag = :tag AND file = :file """
	linksIncStm = """ UPDATE links SET frequency=frequency+1 WHERE w1 = :w1 AND w2 = :w2 AND file = :file """
	linksFindStm = """ SELECT * FROM links WHERE w1 = :w1 AND tag1 = :tag1 AND w2 = :w2 AND tag2 = :tag2 AND file = :file """
	wordFindStm = """ SELECT * FROM words WHERE word = :word AND tag = :tag AND file = :file """
	cursor.execute("""UPDATE words SET frequency=0""")
	cursor.execute("""UPDATE links SET frequency=0""")
	print "DB prepared"
	for f in files:
	    transformParagraphToLine(conPath+f)
	    sqlExec(cursor, fileStm,{"file":f})
	    print "Processing "+f
	    for l in open(conPath+f).readlines():
		print "\t"+l
		tokenedLine = nltk.pos_tag(nltk.word_tokenize(l.replace("."," . ").replace(","," , ").replace("*"," * ").replace("/"," / ")))
		for (i, w) in enumerate(tokenedLine):
		    word = re.sub("[^\w\-\_]", "", w[0]).lower()
		    if word.strip(":-_1234567890"):
			temp ={"word":word, "tag":w[1], "file":f}
			sqlExec(cursor,wordFindStm,temp)
			if cursor.fetchone() is None:
			    sqlExec(cursor,wordStm, temp)
			sqlExec(cursor, wordIncStm,  temp)
			temp=None
			if i < len(tokenedLine)-2:
			  temp = {"w1":word,"tag1":w[1],"w2":re.sub("[^\w\-\_]", "", tokenedLine[i+1][0]).lower(),"tag2":tokenedLine[i+1][1],"file":f}
			  if temp["w2"].strip(":-_1234567890"):
			      sqlExec(cursor, linksFindStm, temp)
			      if cursor.fetchone() is None:
				  sqlExec(cursor, linksStm, temp)
			      sqlExec(cursor, linksIncStm, temp)
			  temp=None
	cursor.execute("""DELETE FROM links WHERE w1=w2 OR  tag1 = "-NONE-" OR tag2 ="-NONE-" """)
	cursor.execute("""DELETE FROM words WHERE tag = "-NONE-" """)
	sqlcon.commit()
	print "Changes committed"





if __name__ == "__main__":
    main(sys.argv[1:])



"""SELECT l1.* , l2.* FROM links l1, links l2 WHERE l1.w1 == l2.w1 AND l2.w2 == l1.w2 AND l1.file == l2. file AND  l1.ROWID != l2.ROWID AND l1.tag1 = l2.tag1 AND l1.tag2=l2.tag2"""#Find Duplicates
"""SELECT * FROM (SELECT * FROM (SELECT * FROM links WHERE length(w1)==1 OR length(w2)==1) WHERE NOT (w1=="a" OR w1=="c" OR w1=="s" OR w1=="i" OR w1=="d")) WHERE NOT (w2=="a" OR w2=="c" OR w2=="s" OR w2=="i" OR w2=="d")"""
"""SELECT * from wordstotal WHERE tag LIKE "N%" OR tag="FW" ORDER BY freq DESC"""
"""SELECT * FROM (SELECT * FROM linkstotal WHERE tag1="FW" OR tag1 LIKE "N%" OR tag1="ADJ") WHERE tag2 LIKE "N%" OR tag2="FW" ORDER BY freq DESC"""
