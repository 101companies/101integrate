import os
import logging #needed for nunning the whole project in debug/info-mode

# the path for the data folder
dataPath = ".."+os.path.sep+".."+os.path.sep+"data"+os.path.sep

# the Path to the configuration-file
configPath = ".."+os.path.sep+"config"+os.path.sep+"config.json"

#the path to the books' folder
bookPath = dataPath + "perbook" + os.path.sep
##
# @param 	a string with the books folder
# @return 	the relative path to the book's metadata folder
def getMetaPath(book):
    return (getBookPath(book)+"metadata"+os.path.sep)
    
##
# @param 	a string with the books folder
# @return 	the relative path to the book's content folder
def getContentPath(book):
    return getBookPath(book)+"contents"+os.path.sep
    
##
# @param 	a string with the books folder
# @return 	the relative path to the book's  folder
def getBookPath(book):
    return (bookPath+book+os.path.sep)

##
# @param 	a string with the books folder
# @return 	the relative path to the book's cache folder 
def getCachePath(book):
    return (getBookPath(book)+os.path.sep+"cache"+os.path.sep)

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
