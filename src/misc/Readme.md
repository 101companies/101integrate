## General
This folder contains general purpose files or those not matching anywhere else

## Files
- csvDiff.py:	Compares two csv Files (used for generated Index Blacklist generation)
- downloader.py:	Downloads indices from googledocs
- downloadnltk.py:	Installs python-nltk corpi (needs user input)
- generateFromStringtemplate.py: 	generates file from Stringtemplate-Group-files (used in alaytics for R-scripts)
- getWikiTerms.py:	Retrieves a list of 101wiki Concepts,Technologies and Languages
- html2text.py:		should replace html2text-binary
- mappingStats.py:	analyses Mappings (which are used in backlink)
- reduceJson.py:	Converts a JSON-file to its "flat" representation


### Script downloader.py

Description: Downloads indecies of terms for the books used

Paramters in order of usage:
* Indexkey for GoogleDocs
* Path to data folder
* List of folders (relative to data folder) to put index files into
