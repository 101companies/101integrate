import os

# the path for the data folder
dataPath = ".."+os.path.sep+".."+os.path.sep+"data"

# the Path to the configuration-file
configPath = "config"+os.path.sep+"config.json"

#the path to the books' folder
bookPath = dataPath + os.path.sep + "perbook"

##
# @param 	a string with the books folder
# @return 	the relative path to the book's metadata folder
# creates the path if it does not exist
def getMetaPath(book):
    path = getBookPath(book)+os.path.sep+"metadata"+os.path.sep
    return path
    
##
# @param 	a string with the books folder
# @return 	the relative path to the book's content folder
def getContentPath(book):
    return getBookPath(book)+"contents"+os.path.sep
    
##
# @param 	a string with the books folder
# @return 	the relative path to the book's  folder
# creates the path if it does not exist
def getBookPath(book):
    path = bookPath+os.path.sep+book
    return path

##
#@param	path	a directory you want to create
# creates a directory if it does not exist
def mkdir(path):
    try:
      os.makedirs(path)
    except OSError:
      pass
    else:
      pass
