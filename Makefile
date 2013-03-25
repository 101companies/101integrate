include src/Makefile.vars

# Books available online
ONLINEBOOKS = RWH LYAH

# Key for Google Docs
INDEXKEY = 0AtMdJdyllDEfdC1YMHE5NmNzNEc3bGx3aV9NbDc2V0E

# Please, read the README.md.
nope:
	@echo Please, read the README.md.

# Download books that are available online
download-books:
	for b in ${ONLINEBOOKS}; do \
		mkdir -p data/perbook/"$$b"/contents; \
		cd src/mining; python crawler.py "$$b" ../../data/perbook/;\
		cd ../..;\
	done
	cd src/mining; make cleanOnlineBooks

# Optionally link offline books, as explained in the README.md
link-books:
	cd data/perbook/PIH; ln -s ~/Dropbox/haskellbooks/clean/PIH/contents
	cd data/perbook/Craft; ln -s ~/Dropbox/haskellbooks/clean/Craft/contents

# Optionally renew google doc data
download-googledocs:
	python src/misc/downloader.py $(INDEXKEY) data/perbook/ LYAH RWH Craft PIH

# Get Python and R tools
download-deps:
	cd src/analytics; make prepare
	src/misc/downloadnltk.py
	sudo easy_install BeautifulSoup
	sudo easy_install nltk
	sudo easy_install inflect
	sudo easy_install html2text
	sudo easy_install gdata
	sudo easy_install jinja2

bootstrap:
	cd src; python bootstrap.py

# Run mining scripts
mine:
	cd src/mining; make mine

# Run analytics scripts
analyze:
	make from-cache
	cd src/analytics; make analyze

# Copies post processed data to cache
from-cache:
	for b in ${NON_LINKED_BOOKS}; do \
		cp data/perbook/$$b/cache/frequenciesMerged.csv  data/perbook/"$$b"/ ;\
		cp data/perbook/$$b/cache/frequenciesDistributionMerged.csv  data/perbook/"$$b"/ ;\
		cp data/perbook/$$b/cache/topFrequency.csv  data/perbook/"$$b"/ ;\
		cp data/perbook/$$b/cache/topScattered.csv  data/perbook/"$$b"/ ;\
		
	done

# Copies post-processed data, required for analytics, to cache
to-cache:
	for b in ${BOOKS}; do \
		cp data/perbook/$$b/frequenciesMerged.csv  data/perbook/"$$b"/cache ;\
		cp data/perbook/$$b/frequenciesDistributionMerged.csv  data/perbook/"$$b"/cache ;\
		cp data/perbook/$$b/topFrequency.csv  data/perbook/"$$b"/cache ;\
		cp data/perbook/$$b/topScattered.csv  data/perbook/"$$b"/cache ;\
	done

# Run backlinking scripts
backlink:
	cd src/mining; make backlink

coverageTables:
	cd src/integrate; make coverageTables


# Clean it all
clean:
	cd data/allbooks; rm -f *.tex *.csv *.json *.png *.html
	for b in ${BOOKS}; do \
		cd data/perbook/"$$b"; rm -rf contents *.tex *.csv *.json *.png *.html ;\
		cd ../../.. ;\
	done
