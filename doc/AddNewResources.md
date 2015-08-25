# Supported Formats

At the moment only html Books are supported.
Most scripts are located in src/mining/.

# Adding Resource

## Prepare Download

* Once you have selected your resource, open src/mining/config. In the templates-subfolder are presets for some systems, if your resource matches one of them (you can lookup some url-matching in matching.json), pick that file as base for further editing. If none matches use HtmlGeneral.json .
* Insert the UrlBase, Extension (, tocUrl if it differs from the UrlBase) and FullName into that json-object.
* Look into config.json and pick a new unique shortie for your resource. It is recommend tho use the first letters of every word in the title. After that insert your json-object into config.json .
* Please add matching tags to your book.
* If the baseUrl of your book is identical to your index-Url, go into src/mining and run ```python metadataGenerator.py $ResourceShortie$``` Please replase `$ResourceShortie$` with the actul shortie.
* Go into data/perbook/$ResourceShortie$/metadata, remove all unwanted sites from chaptersGen.txt/chaptersGen.json and save the chages to capters.txt/chapters.json.
* (optional) Go to src/mining, execute ```python blacklistGenerator.py $ResourceShortie$``` and fill in the values for reason in data/perbook/$ResourceShortie$/metadata/blacklist.json .
* Now run ``` make download-books BOOKS=$ResourceShortie$ ``` and check data/perbook/$ResourceShortie$/contents . If the text files contain unwanted text, analize the html-sourcecode and identify what elements (tags), classes and ids are wrapping that text, then add those unwanted elements, classes and ids to their keys in your resource's object in src/mining/config/config.json and do this instruction again until there is no unwanted text.

## Select terms of Interest

* Download the Resource
* Go into src/mining and run ```python indexGen.py run $ResourceShortie$ ```
* Now go into the Resource's folder, remove all non-wanted Terms (maily verbs and prepositions) from the indexGen.csv and save it as Index.csv in the cache-folder
* Execute ```make indexBlacklist ``` in src/minig
* (optional) add reasons to indexBlacklist.csv in the resource's cache folder

## Select Mapping Terms

* Mine and Analyze the resource
* (optional) run ``` python get wikiTerms.py ``` in src/misc
* run ``` make mappingTerms.py ``` 
* now a mappings.csv should be in the Resource's metadata-folder
* edit that file to match the external Ontology (if you made the optinal second step some terms which are already in the 101ontology will be already mapped to identical ontology-terms, please check the as well)

## Final
* Run the full Integration-Cycle and check your results for errors
* If you find none add the production-Tag to your resource's tag list
