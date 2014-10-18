import nltk
import sqlite3 as sql
import os
import sys
import re
import constants
from sortedcontainers import SortedSet

def sqlExec(cursor, statement, values):
  try:
	cursor.execute(statement, values)
  except sqlite.IntegrityError, e:
	print e
  else:
	pass  
      
def normalizeWord(word):
  return re.sub("[^\w\-\_]", " ", word.lower()).replace("\r","").replace("\n","")


def transformParagraphToLine(path):
    temp = ""
    for l in open(path).readlines():
	  if not l.replace(" ","").replace("\t","").replace("\r","").replace("\n",""):
	      temp +="\r\n \r\n"
	  else:
	      temp += " "+l.replace("\r","").replace("\n","")
    writer = open(path, "w")
    writer.write(temp)
    writer.close

##
# @DEPRECATED
def insertOldDb(args):
      for a in args:
	conPath = constants.getContentPath(a)
	files = os.listdir(conPath)
	sqlcon = sqlite.connect(constants.getBookPath(a)+"Entries.db")
	sqlcon.text_factory = str
	cursor = sqlcon.cursor()
	print "connected to DB"
	#remove old data
	cursor.execute(""" DROP VIEW IF EXIST linkstotal """)
	cursor.execute(""" DROP VIEW IF EXIST wordstotal """)
	cursor.execute(""" DROP TABLE IF EXIST links """)
	cursor.execute(""" DROP TABLE IF EXIST words """)
	cursor.execute(""" DROP TABLE IF EXIST files """)
	#setup database
	cursor.execute(""" CREATE TABLE IF NOT EXISTS words ( word TEXT , tag TEXT, file TEXT, frequency INTEGER)""")
	cursor.execute(""" CREATE TABLE IF NOT EXISTS files(file TEXT PRIMARY KEY)""")
	cursor.execute(""" CREATE TABLE IF NOT EXISTS links(w1 TEXT, tag1 TEXT, w2 TEXT, tag2 TEXT, file TEXT, frequency INTEGER)""")
	#cursor.execute(""" CREATE TABLE IF NOT EXISTS wordorder(n1 INTEGER, n2 INTEGER, file TEXT, frequency INTEGER)""")
	cursor.execute(""" CREATE VIEW IF NOT EXISTS linkstotal as SELECT w1, w2, tag1, tag2, SUM(frequency) as freq FROM links GROUP BY w1, w2, tag1, tag2""")
	cursor.execute(""" CREATE VIEW IF NOT EXISTS wordstotal as SELECT word, tag, SUM(frequency) as freq FROM words GROUP BY word, tag""")
	#prepare Statements
	fileStm = """INSERT INTO files(file) VALUES(:file)  """
	wordStm = """INSERT INTO words(word, tag, file, frequency) VALUES(:word, :tag, :file , 0 )"""
	linksStm = """ INSERT INTO links(w1,tag1, w2, tag2, file, frequency) VALUES(:w1 , :tag1 , :w2 , :tag2 , :file , 0) """
	wordIncStm = """ UPDATE words SET frequency=frequency+1 WHERE word = :word AND tag = :tag AND file = :file """
	linksIncStm = """ UPDATE links SET frequency=frequency+1 WHERE w1 = :w1 AND w2 = :w2 AND file = :file """
	linksFindStm = """ SELECT * FROM links WHERE w1 = :w1 AND tag1 = :tag1 AND w2 = :w2 AND tag2 = :tag2 AND file = :file """
	wordFindStm = """ SELECT * FROM words WHERE word = :word AND tag = :tag AND file = :file """
	print "DB prepared"
	for f in files:
	    transformParagraphToLine(conPath+f)
	    sqlExec(cursor, fileStm,{"file":f})
	    print "Processing "+f
	    for l in open(conPath+f).readlines():
		print "\t"+l
		tokenedLine = nltk.pos_tag(nltk.word_tokenize(l.replace("."," . ").replace(","," , ").replace("*"," * ").replace("/"," / ")))
		for (i, w) in enumerate(tokenedLine):
		    word = normalizeWord(w[0])
		    if word.strip(":-_1234567890"):
			temp ={"word":word, "tag":w[1], "file":f}
			sqlExec(cursor,wordFindStm,temp)
			if cursor.fetchone() is None:
			    sqlExec(cursor,wordStm, temp)
			sqlExec(cursor, wordIncStm,  temp)
			temp=None
			if i < len(tokenedLine)-2:
			  temp = {"w1":word,"tag1":w[1],"w2":normalizeWord(tokenedLine[i+1][0]),"tag2":tokenedLine[i+1][1],"file":f}
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

def insertIfNotExists(cursor, lookupStm, insertStm, dictionary):
    cursor.execute(lookupStm, dictionary)
    temp = cursor.fetchone()
    if temp is None:
      cursor.execute(insertStm, dictionary)
      cursor.execute(lookupStm, dictionary)
      temp = cursor.fetchone()[0]
    else:
      temp = temp[0]
    return temp

def genDB(sqlcon, book, files):
	sqlcon.text_factory = str
	cursor = sqlcon.cursor()
	print "connected to DB"
	#Remove old data
	cursor.execute("""DROP VIEW IF EXISTS CommonNounsPerFile""")
	cursor.execute("""DROP VIEW IF EXISTS CommonTupelsWNouns""")
	cursor.execute("""DROP VIEW IF EXISTS TupelsWNounsPerFile""")
	cursor.execute("""DROP VIEW IF EXISTS TupelOverwiew""")
	cursor.execute("""DROP VIEW IF EXISTS TupelFreq """)
	cursor.execute("""DROP VIEW IF EXISTS WordFreq""")
	cursor.execute("""DROP VIEW IF EXISTS CommonNouns""")
	cursor.execute("""DROP VIEW IF EXISTS WordOverview """)
	cursor.execute("""DROP TABLE IF EXISTS FreqTupels""")
	cursor.execute("""DROP TABLE IF EXISTS TupelTags""")
	cursor.execute("""DROP TABLE IF EXISTS Tupels""")
	cursor.execute("""DROP TABLE IF EXISTS FreqSingle""")
	cursor.execute("""DROP TABLE IF EXISTS Files""")
	cursor.execute("""DROP TABLE IF EXISTS Words""")
	print "Deleted old Data (if any)"
	#setup DB
	cursor.execute("""CREATE TABLE IF NOT EXISTS Words (ID INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS Files (ID INTEGER PRIMARY KEY AUTOINCREMENT, file TEXT)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS FreqSingle(word INTEGER,  tag TEXT, file TEXT, freq INTEGER DEFAULT 0, FOREIGN KEY(file) REFERENCES Files(file), FOREIGN KEY(word) REFERENCES Words(ID))""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS Tupels(ID INTEGER PRIMARY KEY AUTOINCREMENT, w1 INTEGER, w2 INTEGER, FOREIGN KEY(w2) REFERENCES Words(ROWID) , FOREIGN KEY(w1) REFERENCES Words(ID))""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS TupelTags(ID INTEGER PRIMARY KEY AUTOINCREMENT, tupel INTEGER, tag1 TEXT, tag2 TEXT , FOREIGN KEY(tupel) REFERENCES Tupels(ROWID))""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS FreqTupels(tupel INTEGER, tagID INTEGER, freq NUMERIC DEFAULT 0, file TEXT, FOREIGN KEY(file) REFERENCES Files(file), FOREIGN KEY(tupel) REFERENCES Tupels(ID), FOREIGN KEY(tagID) REFERENCES TupelTags(ID)) """)
	print "Tables created"
	cursor.execute("""CREATE VIEW IF NOT EXISTS TupelOverwiew AS SELECT * FROM Words w1, Words w2, Tupels t , TupelTags tt, FreqTupels ft WHERE w1.ID = t.w1 AND w2.ID = t.w2 AND tt.tupel=t.ID AND ft.tagID=tt.ID""")
	cursor.execute("""CREATE VIEW IF NOT EXISTS TupelFreq AS SELECT t.ID as tID, w1.word as word1, w2.word as word2, SUM(f.freq) as freq FROM Words w1, Words w2, Tupels t, FreqTupels f WHERE w1.ID == t.w1 AND w2.ID == t.w2 AND t.ID == f.tupel GROUP BY t.ID """)
	cursor.execute("""CREATE VIEW IF NOT EXISTS WordFreq AS SELECT w.* , SUM(f.freq) as freq FROM Words w, FreqSingle f WHERE w.ID = f.word GROUP BY w.ID""")
	cursor.execute("""CREATE VIEW IF NOT EXISTS CommonNouns AS SELECT DISTINCT w.* FROM WordFreq w, (SELECT word as ID FROM FreqSingle WHERE tag LIKE "NN%" AND freq > 1) i WHERE i.ID = w.ID ORDER BY w.freq DESC""")
	cursor.execute("""CREATE VIEW IF NOT EXISTS CommonTupelsWNouns AS SELECT DISTINCT t.* FROM TupelFreq t, (SELECT tupel FROM TupelTags WHERE (tag1 LIKE "NN%" OR tag1 LIKE "JJ%") AND tag2 LIKE "NN%") i WHERE t.tID == i.tupel ORDER BY t.freq DESC""")
	cursor.execute("""CREATE VIEW IF NOT EXISTS WordOverview AS SELECT * FROM Words w, FreqSingle f WHERE w.ID = f.word""")
	cursor.execute("""CREATE VIEW IF NOT EXISTS TupelsWNounsPerFile AS SELECT DISTINCT w1.word as w1, w2.word as w2, f. file, sum(freq) AS freq FROM Words w1, Words w2, Tupels t, TupelTags tt, FreqTupels f WHERE w1.ID = t.w1 AND w2.ID = t.w2 AND t.ID = f.tupel AND tt.tupel = t.ID AND (tt.tag1 LIKE "NN%" OR tt.tag1 LIKE "JJ%") AND tt.tag2 LIKE "NN%" GROUP BY f.tupel, f.file ORDER BY sum(freq) DESC """)
	cursor.execute("""CREATE VIEW IF NOT EXISTS CommonNounsPerFile AS SELECT w.ID as wID, w.word, f.file, sum(f.freq) as freq FROM Words w, FreqSingle f , (SELECT word FROM FreqSingle WHERE tag LIKE "NN%") s WHERE w.ID =f.word AND f.word = s.word GROUP BY f.file, f.word  ORDER BY sum(freq) DESC""")
	
	print "Views added"
	#prepare Statements
	#Selection
	wordIdStm = """SELECT ID FROM Words WHERE word = :word"""
	fileIdStm = """SELECT ID FROM Files WHERE file = :file"""
	tupelIdStm = """SELECT ID FROM Tupels WHERE w1 = :wId1 AND w2 = :wId2"""
	tupelTagIdStm = """ SELECT ID FROM  TupelTags WHERE tag1 = :tag1 AND tag2 = :tag2 AND tupel = :tId"""
	freqTTStm = """ SELECT freq FROM FreqTupels WHERE tagID = :tagId AND file = :file  AND tupel = :tId"""
	freqWordStm = """ SELECT freq FROM FreqSingle WHERE word = :wId1 AND tag = :tag1 AND file = :file"""
	#Insertion
	wordInsStm = """ INSERT INTO Words(word) VALUES( :word)"""
	fileInsStm = """ INSERT INTO Files(file) VALUES( :file)"""
	tupelInsStm = """ INSERT INTO Tupels(w1, w2) VALUES( :wId1, :wId2)"""
	tupelTagInsStm = """ INSERT INTO TupelTags(tupel, tag1, tag2) VALUES( :tId, :tag1, :tag2) """
	freqTTInsStm = """ INSERT INTO FreqTupels(tupel, tagID, file) VALUES( :tId, :tagId, :file)"""
	freqWordInsStm = """ INSERT INTO FreqSingle(word, tag, file) VALUES( :wId1, :tag1, :file) """
	#Update
	freqWordIncStm = """ UPDATE FreqSingle SET freq=freq+1 WHERE word = :wId1 AND tag = :tag1 AND file = :file """
	freqTTIncStm = """ UPDATE FreqTupels SET freq=freq+1 WHERE tupel = :tId AND tagId = :tagId AND file = :file """
	print "prepared Statements"
	for f in files:
	      print "Processing "+f
	      transformParagraphToLine(conPath+f)
	      temp =  {"file" : f}
	      cursor.execute(fileIdStm, temp)
	      insertIfNotExists(cursor, fileIdStm, fileInsStm, temp)
	      temp['file']= f
	      for l in open(conPath+f).readlines():
			for s in l.split("."):
				tokenedSentence = nltk.pos_tag(nltk.word_tokenize(re.sub("[^,:\w\-\_\.\s]", " ", s.replace("."," . ").replace(","," , ").replace("*"," * ").replace("/"," / "))))
				for (i, w) in enumerate(tokenedSentence):
					word = normalizeWord(w[0])
					if (len(word.strip(":-_1234567890"))<=1):
						continue
					temp['w1'] = word
					temp['wId1'] = str(insertIfNotExists(cursor, wordIdStm, wordInsStm, {'word':word}))
					temp['tag1'] = w[1]
					insertIfNotExists(cursor, freqWordStm, freqWordInsStm, temp)
					cursor.execute(freqWordIncStm, temp)
					if i < len(tokenedSentence)-2:
						temp['w2'] = normalizeWord(tokenedSentence[i+1][0])
						if len(temp['w2'].strip(":-_1234567890")) > 1:
							temp['wId2'] = str(insertIfNotExists(cursor, wordIdStm, wordInsStm, {'word':temp['w2']}))
							temp['tag2'] = tokenedSentence[i+1][1]
							temp['tId'] =  str(insertIfNotExists(cursor, tupelIdStm, tupelInsStm, {'wId1':temp['wId1'],'wId2':temp['wId2']}))
							temp['tagId'] = str(insertIfNotExists(cursor, tupelTagIdStm, tupelTagInsStm, {'tId':temp['tId'],'tag1':temp['tag1'],'tag2':temp['tag2']}))
							insertIfNotExists(cursor, freqTTStm, freqTTInsStm, {'tagId':temp['tagId'], 'file':temp['file'],'tId':temp['tId']})
							cursor.execute(freqTTIncStm, {'tagId':temp['tagId'], 'file':temp['file'], 'tId':temp['tId']})
	sqlcon.commit()
	print "data committed to db"

def selectTerms(sqlcon, book,files):
	cursor = sqlcon.cursor()
	cursor.execute("""SELECT word FROM CommonNouns WHERE freq > 1 AND freq >= (SELECT freq FROM CommonNouns ORDER BY freq DESC LIMIT 1 OFFSET 50)  ORDER BY freq DESC""")
	words = SortedSet() #TODO switch back to set once word filtering is acceptable
	temp = cursor.fetchone()
	while (temp is not None):
	  words.add(temp[0])
	  temp = cursor.fetchone()
	cursor.execute("""SELECT word1, word2 FROM CommonTupelsWNouns WHERE freq > 1 AND freq >= (SELECT freq FROM CommonTupelsWNouns ORDER BY freq DESC LIMIT 1 OFFSET 50)   ORDER BY freq DESC""")
	temp = cursor.fetchone()
	while (temp is not None):
	  words.add(temp[0]+" "+temp[1])
	  temp = cursor.fetchone()
	wordFetchStm = """SELECT word FROM CommonNounsPerFile WHERE file = :file AND freq > 1 AND freq >= (SELECT freq FROM CommonNounsPerFile WHERE file = :file ORDER BY freq DESC LIMIT 1 OFFSET 20) ORDER BY freq DESC"""
	tupelFetchStm = """SELECT w1, w2 FROM TupelsWNounsPerFile WHERE file = :file AND freq > 1 AND freq >= (SELECT freq FROM TupelsWNounsPerFile WHERE file = :file ORDER BY freq DESC LIMIT 1 OFFSET 20) ORDER BY freq DESC LIMIT 10"""
	for f in files:
	  cursor.execute(wordFetchStm, {'file':f})
	  temp = cursor.fetchone()
	  while (temp is not None):
	    words.add(temp[0])
	    temp = cursor.fetchone()
	  cursor.execute(tupelFetchStm, {'file':f})
	  temp = cursor.fetchone()
	  while (temp is not None):
	    words.add(temp[0]+" "+temp[1])
	    temp = cursor.fetchone()
	sqlcon.close()
	print "Fetched Data from DB"
	path = constants.getCachePath(book)
	constants.mkdir(path)
	writer = open(path+"IndexGen.csv","w")
	for w in words:
	  writer.write(w)
	  writer.write("\n")
	print "Created IndexGen.csv"

def main(args):
 if len(args) < 1:
	print "Exiting"
 for a in args:
	print "Processing " + a
	conPath = constants.getContentPath(a)
	files = os.listdir(conPath)
	sqlcon = sqlite.connect(constants.getBookPath(a)+"Frequencies.db")
	sqlcon.text_factory = str
	cursor = sqlcon.cursor()
	print "connected to DB"
	#Remove old data
	cursor.execute("""DROP VIEW IF EXISTS CommonNounsPerFile""")
	cursor.execute("""DROP VIEW IF EXISTS CommonTupelsWNouns""")
	cursor.execute("""DROP VIEW IF EXISTS TupelsWNounsPerFile""")
	cursor.execute("""DROP VIEW IF EXISTS TupelOverwiew""")
	cursor.execute("""DROP VIEW IF EXISTS TupelFreq """)
	cursor.execute("""DROP VIEW IF EXISTS WordFreq""")
	cursor.execute("""DROP VIEW IF EXISTS CommonNouns""")

	cursor.execute("""DROP VIEW IF EXISTS WordOverview """)
	cursor.execute("""DROP TABLE IF EXISTS FreqTupels""")
	cursor.execute("""DROP TABLE IF EXISTS TupelTags""")
	cursor.execute("""DROP TABLE IF EXISTS Tupels""")
	cursor.execute("""DROP TABLE IF EXISTS FreqSingle""")
	cursor.execute("""DROP TABLE IF EXISTS Files""")
	cursor.execute("""DROP TABLE IF EXISTS Words""")
	print "Deleted old Data (if any)"
	#setup DB
	cursor.execute("""CREATE TABLE IF NOT EXISTS Words (ID INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS Files (ID INTEGER PRIMARY KEY AUTOINCREMENT, file TEXT)""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS FreqSingle(word INTEGER,  tag TEXT, file TEXT, freq INTEGER DEFAULT 0, FOREIGN KEY(file) REFERENCES Files(file), FOREIGN KEY(word) REFERENCES Words(ID))""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS Tupels(ID INTEGER PRIMARY KEY AUTOINCREMENT, w1 INTEGER, w2 INTEGER, FOREIGN KEY(w2) REFERENCES Words(ROWID) , FOREIGN KEY(w1) REFERENCES Words(ID))""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS TupelTags(ID INTEGER PRIMARY KEY AUTOINCREMENT, tupel INTEGER, tag1 TEXT, tag2 TEXT , FOREIGN KEY(tupel) REFERENCES Tupels(ROWID))""")
	cursor.execute("""CREATE TABLE IF NOT EXISTS FreqTupels(tupel INTEGER, tagID INTEGER, freq NUMERIC DEFAULT 0, file TEXT, FOREIGN KEY(file) REFERENCES Files(file), FOREIGN KEY(tupel) REFERENCES Tupels(ID), FOREIGN KEY(tagID) REFERENCES TupelTags(ID)) """)
	print "Tables created"
	cursor.execute("""CREATE VIEW IF NOT EXISTS TupelOverwiew AS SELECT * FROM Words w1, Words w2, Tupels t , TupelTags tt, FreqTupels ft WHERE w1.ID = t.w1 AND w2.ID = t.w2 AND tt.tupel=t.ID AND ft.tagID=tt.ID""")
	cursor.execute("""CREATE VIEW IF NOT EXISTS TupelFreq AS SELECT t.ID as tID, w1.word as word1, w2.word as word2, SUM(f.freq) as freq FROM Words w1, Words w2, Tupels t, FreqTupels f WHERE w1.ID == t.w1 AND w2.ID == t.w2 AND t.ID == f.tupel GROUP BY t.ID """)
	cursor.execute("""CREATE VIEW IF NOT EXISTS WordFreq AS SELECT w.* , SUM(f.freq) as freq FROM Words w, FreqSingle f WHERE w.ID = f.word GROUP BY w.ID""")
	cursor.execute("""CREATE VIEW IF NOT EXISTS CommonNouns AS SELECT DISTINCT w.* FROM WordFreq w, (SELECT word as ID FROM FreqSingle WHERE tag LIKE "NN%" AND freq > 1) i WHERE i.ID = w.ID ORDER BY w.freq DESC""")
	cursor.execute("""CREATE VIEW IF NOT EXISTS CommonTupelsWNouns AS SELECT DISTINCT t.* FROM TupelFreq t, (SELECT tupel FROM TupelTags WHERE (tag1 LIKE "NN%" OR tag1 LIKE "JJ%") AND tag2 LIKE "NN%") i WHERE t.tID == i.tupel ORDER BY t.freq DESC""")
	cursor.execute("""CREATE VIEW IF NOT EXISTS WordOverview AS SELECT * FROM Words w, FreqSingle f WHERE w.ID = f.word""")
	cursor.execute("""CREATE VIEW IF NOT EXISTS TupelsWNounsPerFile AS SELECT DISTINCT w1.word as w1, w2.word as w2, f. file, sum(freq) AS freq FROM Words w1, Words w2, Tupels t, TupelTags tt, FreqTupels f WHERE w1.ID = t.w1 AND w2.ID = t.w2 AND t.ID = f.tupel AND tt.tupel = t.ID AND (tt.tag1 LIKE "NN%" OR tt.tag1 LIKE "JJ%") AND tt.tag2 LIKE "NN%" GROUP BY f.tupel, f.file ORDER BY sum(freq) DESC """)
	cursor.execute("""CREATE VIEW IF NOT EXISTS CommonNounsPerFile AS SELECT w.ID as wID, w.word, f.file, sum(f.freq) as freq FROM Words w, FreqSingle f , (SELECT word FROM FreqSingle WHERE tag LIKE "NN%") s WHERE w.ID =f.word AND f.word = s.word GROUP BY f.file, f.word  ORDER BY sum(freq) DESC""")
	
	print "Views added"
	#prepare Statements
	#Selection
	wordIdStm = """SELECT ID FROM Words WHERE word = :word"""
	fileIdStm = """SELECT ID FROM Files WHERE file = :file"""
	tupelIdStm = """SELECT ID FROM Tupels WHERE w1 = :wId1 AND w2 = :wId2"""
	tupelTagIdStm = """ SELECT ID FROM  TupelTags WHERE tag1 = :tag1 AND tag2 = :tag2 AND tupel = :tId"""
	freqTTStm = """ SELECT freq FROM FreqTupels WHERE tagID = :tagId AND file = :file  AND tupel = :tId"""
	freqWordStm = """ SELECT freq FROM FreqSingle WHERE word = :wId1 AND tag = :tag1 AND file = :file"""
	#Insertion
	wordInsStm = """ INSERT INTO Words(word) VALUES( :word)"""
	fileInsStm = """ INSERT INTO Files(file) VALUES( :file)"""
	tupelInsStm = """ INSERT INTO Tupels(w1, w2) VALUES( :wId1, :wId2)"""
	tupelTagInsStm = """ INSERT INTO TupelTags(tupel, tag1, tag2) VALUES( :tId, :tag1, :tag2) """
	freqTTInsStm = """ INSERT INTO FreqTupels(tupel, tagID, file) VALUES( :tId, :tagId, :file)"""
	freqWordInsStm = """ INSERT INTO FreqSingle(word, tag, file) VALUES( :wId1, :tag1, :file) """
	#Update
	freqWordIncStm = """ UPDATE FreqSingle SET freq=freq+1 WHERE word = :wId1 AND tag = :tag1 AND file = :file """
	freqTTIncStm = """ UPDATE FreqTupels SET freq=freq+1 WHERE tupel = :tId AND tagId = :tagId AND file = :file """
	print "prepared Statements"
	for f in files:
	      print "Processing "+f
	      transformParagraphToLine(conPath+f)
	      temp =  {"file" : f}
	      cursor.execute(fileIdStm, temp)
	      insertIfNotExists(cursor, fileIdStm, fileInsStm, temp)
	      temp['file']= f
	      for l in open(conPath+f).readlines():
		      tokenedLine = nltk.pos_tag(nltk.word_tokenize(re.sub("[^,:\w\-\_\.\s]", " ", l.replace("."," . ").replace(","," , ").replace("*"," * ").replace("/"," / "))))
		      for (i, w) in enumerate(tokenedLine):
			word = normalizeWord(w[0])
			if (len(word.strip(":-_1234567890"))<=1):
			  continue
			temp['w1'] = word
			temp['wId1'] = str(insertIfNotExists(cursor, wordIdStm, wordInsStm, {'word':word}))
			temp['tag1'] = simplify_wsj_tag(w[1])
			insertIfNotExists(cursor, freqWordStm, freqWordInsStm, temp)
			cursor.execute(freqWordIncStm, temp)
			if i < len(tokenedLine)-2:
				temp['w2'] = normalizeWord(tokenedLine[i+1][0])
				if len(temp['w2'].strip(":-_1234567890")) > 1:
					temp['wId2'] = str(insertIfNotExists(cursor, wordIdStm, wordInsStm, {'word':temp['w2']}))
					temp['tag2'] = simplify_wsj_tag(tokenedLine[i+1][1])
					temp['tId'] =  str(insertIfNotExists(cursor, tupelIdStm, tupelInsStm, {'wId1':temp['wId1'],'wId2':temp['wId2']}))
					temp['tagId'] = str(insertIfNotExists(cursor, tupelTagIdStm, tupelTagInsStm, {'tId':temp['tId'],'tag1':temp['tag1'],'tag2':temp['tag2']}))
					insertIfNotExists(cursor, freqTTStm, freqTTInsStm, {'tagId':temp['tagId'], 'file':temp['file'],'tId':temp['tId']})
					cursor.execute(freqTTIncStm, {'tagId':temp['tagId'], 'file':temp['file'], 'tId':temp['tId']})
	sqlcon.commit()
	print "data committed to db"
	cursor.execute("""SELECT word FROM CommonNouns ORDER BY freq DESC LIMIT 25""")
	words = SortedSet() #TODO switch back to set once word filtering is acceptable
	temp = cursor.fetchone()
	while (temp is not None):
	  words.add(temp[0])
	  temp = cursor.fetchone()
	cursor.execute("""SELECT word1, word2 FROM CommonTupelsWNouns ORDER BY freq DESC LIMIT 25""")
	temp = cursor.fetchone()
	while (temp is not None):
	  words.add(temp[0]+" "+temp[1])
	  temp = cursor.fetchone()
	wordFetchStm = """SELECT word FROM CommonNounsPerFile WHERE file = :file ORDER BY freq DESC LIMIT 10"""
	tupelFetchStm = """SELECT w1, w2 FROM TupelsWNounsPerFile WHERE file = :file ORDER BY freq DESC LIMIT 10"""
	for f in files:
	  cursor.execute(wordFetchStm, {'file':f})
	  temp = cursor.fetchone()
	  while (temp is not None):
	    words.add(temp[0])
	    temp = cursor.fetchone()
	  cursor.execute(tupelFetchStm, {'file':f})
	  temp = cursor.fetchone()
	  while (temp is not None):
	    words.add(temp[0]+" "+temp[1])
	    temp = cursor.fetchone()
	sqlcon.close()
	print "Fetched Data from DB"
	path = constants.getCachePath(a)
	constants.mkdir(path)
	writer = open(path+"IndexGen.csv","w")
	for w in words:
	  writer.write(w)
	  writer.write("\n")
	print "Created IndexGen.csv"


if __name__ == "__main__":
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		print "exiting"
	elif len(sys.argv) > 1 or len(sys.argv) < 4:
		book = sys.argv[1]
		print "Processing " + book
		conPath = constants.getContentPath(book)
		files = os.listdir(conPath)
		sqlcon = sql.connect(constants.getBookPath(book)+"Frequencies.db")
		mode = None
		if len(sys.argv) == 3:
			mode = sys.argv[2]
		if mode == None:
			genDB(sqlcon, book,files)
			selectTerms(sqlcon, book,files)
		elif mode == "generate":
			genDB(sqlcon, book,files)
		elif mode == "select":
			selectTerms(sqlcon, book,files)
		else:
			print mode + " not recognized"


#old db schema
"""SELECT l1.* , l2.* FROM links l1, links l2 WHERE l1.w1 == l2.w1 AND l2.w2 == l1.w2 AND l1.file == l2. file AND  l1.ROWID != l2.ROWID AND l1.tag1 = l2.tag1 AND l1.tag2=l2.tag2"""#Find Duplicates
"""SELECT * FROM (SELECT * FROM (SELECT * FROM links WHERE length(w1)==1 OR length(w2)==1) WHERE NOT (w1=="a" OR w1=="c" OR w1=="s" OR w1=="i" OR w1=="d")) WHERE NOT (w2=="a" OR w2=="c" OR w2=="s" OR w2=="i" OR w2=="d")"""
"""SELECT * from wordstotal WHERE tag LIKE "NN%" OR tag="FW" ORDER BY freq DESC"""
"""SELECT * FROM (SELECT * FROM linkstotal WHERE tag1="FW" OR tag1 LIKE "NN%" OR tag1="JJ%") WHERE tag2 LIKE "NN%" OR tag2="FW" ORDER BY freq DESC"""
