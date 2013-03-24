# Books available online
ONLINEBOOKS = RWH LYAH

# Books not available online
OFFLINEBOOKS = PIH Craft

# All books
ALLBOOKS = ${ONLINEBOOKS} ${OFFLINEBOOKS}

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

# Run mining scripts
mine:
	cd src/mining; make mine

# Run analytics scripts
analyze:
	cd src/analytics; make analyze

# Run backlinking scripts
backlink:
	cd src/mining; make backlink

coverageTables:
	cd src/integrate; make coverageTables


# Clean it all
clean:
	cd data/allbooks; rm -f *.tex *.csv *.json *.png *.html
	for b in ${ALLBOOKS}; do \
		cd data/perbook/"$$b"; rm -rf contents *.tex *.csv *.json *.png *.html ;\
		cd ../../.. ;\
	done
