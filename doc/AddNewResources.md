# Supported Formats

At the moment only html Books are supported.
All scripts are located in src/mining/.

# Adding Resource

## Prepare Download

* Once you have selected your resource, open src/mining/config. In the templates-subfolder are presets for some systems, if your resource matches one of them (you can lookup some url-maiching in matching.json), pick that file as base for further editing. If none matches use HtmlGeneral.json .
* Insert the UrlBase and FullName into that json-object.
* Look into config.json and pick a new unique shortie for your resource. It is recommend tho use the first letters of every word in the title. After that insert your json-object into config.json .
* Please add matching tags to your book.
* If the baseUrl of your book is identical to your index-Url, go into src/mining and run ```python metadataGenerator.py $ResourceShortie$``` Please replase `$ResourceShortie$` with the actul shortie.
* Go into data/perbook/$ResourceShortie$/metadata, remove all unwanted sites from chaptersGen.txt/chaptersGen.json and save the chages to capters.txt/chapters.json.
* (optional) Go to src/mining, execute ```python blacklistGenerator.py $ResourceShortie$``` and fill in the values for reason in data/perbook/$ResourceShortie$/metadata/blacklist.json .
* Now run ``` make download-books BOOKS=$ResourceShortie$ ``` and check data/perbook/$ResourceShortie$/contents . If the text files contain unwanted text, analize the html-sourcecode and identify what elements (tags), classes and ids are wrapping that text, then add those unwanted elements, classes and ids to their keys in your resource's object in src/mining/config/config.json and do this instruction again until there is no unwanted text.

## Select terms of Interest

TODO
