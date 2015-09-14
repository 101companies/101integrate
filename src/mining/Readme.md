# General

This folder contains files for the mining- and backlinking-phase.

# Files

- backlinksMapper.py:		Term-chapter-mapping 
- blacklistGeneratorMetaData.py: Generate the the chapter blacklist for unused book-chapters
- bookDownloader.py:	Selects the to be downloaded-books and downloads them using the crawler
- constants.py:		path-variables
- crawler.py:		Downloads books
- FlatWiki.hs:		Retrieves Haskell-related data from the 101 wiki (broken)
- frequencies.py:	Gets frequencies of terms in the resources
- frequencyCounter.py:	Generates FrequenciyOverview (unused & broken)
- indexGen.py:		generates a Book index from content using Technical Term Recognition
- lists2tex.py:		Converts 101wiki csv-files to tex
- mappingTerms.py:	Generates a list of to-be-mapped Terms
- merge.py:		Merges/cleanes indicies
- mergeBacklinks.py:	combines Backlinks of linkable books
- metadataGenerator.py:	generates the chapter-data necessary for book downloading
- patternCleaner.py:	used in merge.py, cleans terms 
- ranker.py:		gets the list of common English words from wordnet
- spliter.py:		splits tex-books in seperte chapter-files
- texCleaner.py:	cleans tex-files

# Detailed Description

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
* "merged" | "nonmerged"

## Script backlinksMapper.py

Description: Computes files for backlinks from terms to resouces
Paramters in order of usage:
* Name of the resource
* Base path to datafolder for resources
* Name of frequency file (relative to resource path)
* Name of content folder (relative to resource path)

