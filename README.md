# Summary

This repo contributes to the 101companies Project. 101integrate is a framework for the integration of knowledge resources. At this point, the framework specifically addresses vocabulary integration and cross-referencing betweem Haskell textbooks and 101wiki. Currently, 4 Haskell textbooks are supported.

# Tool dependencies

Make sure all dependencies are installed.

You need System R: http://www.r-project.org/

You need a bunch of Python packages and some NLP support.

This is taken care of by this command:

    make download-deps

When the NLTK downloader pops up, select all corpora for download.

# Online textbooks

Some of the supported textbooks are available online. They are not included into the repo. They must be downloaded with the following command:

    make download-books
    
The following book-packages can be chosen: Haskell

You can download e.g. the Haskell-Book-Package with the following command:

    make download-books BOOKS="haskell"

# Offline textbooks

2 of the supported textbooks are not available online. If you have offline access to them, please link them as demonstrated by the make target "link-books". That is, if the books' sources are available per a "haskellbooks" folder in your dropbox, then the following command suffices:

    make link-books

Most likely, you don't have access to the books' sources. In this case, the scripts need to be adjusted to ignore these books. We will make the process adaptive so that you don't need to bother, but for the moment you need to.

# Mining and analyzing

Run these commands:

    make mine
    make analyze

These commands will create various data files in data/allbooks and data/perbook/*.

# Mining phase

See folder "mining" for the scripts.

## Script downloader.py

Description: Downloads indecies of terms for the books used

Paramters in order of usage:
* Indexkey for GoogleDocs
* Path to data folder
* List of folders (relative to data folder) to put index files into

## Script merge.py

Description: Merges and cleans a list of given index files. Creates clean index and optionally a file of crosscut betweens given indecies.

Paramters in order of usage:
* Base path of datafolder
* Base path of inputfolder
* Path of resources (relative to data path + input path)
* Path of index files relative to data path + input path + resource name)
* Path of merged index file (relative to data path)
* Path of metaindex file (relative to data path)
* Number n of common English words to ignore
* "nocrosscut" | Path to crosscut file (relative to data path)

## Script frequencies.py

Description: Computes frequencies of words for a given set of terms in a given set of resourcesmerged; \
Paramters in order of usage:
* Name of the resource
* Base path to datafolder
* Base path of resource (relative to data path)
* Base path of index folder (relative to data path)
* Name of index file (relative to index path)
* Name of chapters file (relative to resource path)
* Name of content folder (relative to resource path)
* Name of metaindex file (relative to index path)

## Script backlinksMapper.py

Description: Computes files for backlinks from terms to resouces
Paramters in order of usage:
* Name of the resource
* Base path to datafolder for resources
* Name of frequency file (relative to resource path)
* Name of content folder (relative to resource path)

All other scripts are only used indirectly.

## Analytics phase

See folder "analytics" for the scripts.

TODO
