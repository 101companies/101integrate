# Summary

This repo contributes to the 101companies Project. 101integrate is a framework for the integration of knowledge resources. At this point, the framework specifically addresses vocabulary integration and cross-referencing betweem Haskell textbooks and 101wiki.

# Non-online resources

2 out of 4 Haskell books are not available online. If you have offline access to them, please link them as follows. We assume that the books' sources are available per a "haskellbooks" folder. For example, you may have this folder in your Dropbox directory.

    cd data/perbook/PIH
    ln -s ~/Dropbox/haskellbooks/clean/PIH/contents
    cd ../Craft
    ln -s ~/Dropbox/haskellbooks/clean/Craft/contents

# Tool dependencies

Make sure all dependencies are installed.

You need System R: http://www.r-project.org/

Execute these commands:

    cd src
    make download-deps

When the NLTK downloader pops up, select all corpora for download.

# Mining and analyzing

    make mine
    make analyze

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
