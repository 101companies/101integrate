# Books available online
ONLINEBOOKS = RWH LYAH

# Key for Google Docs
INDEXKEY = 0AtMdJdyllDEfdC1YMHE5NmNzNEc3bGx3aV9NbDc2V0E

# Please, read the README.md.
nope:
	@echo Please, read the README.md.
	
	
run:
	make download-books
	make bootstrap
	make mine
	make from-cache
	make analyze
	make backlink
	cd src/integrate; make integrate

# Download books that are available online
download-books:
	# cd src/mining; make cleanOnlineBooks
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
	cd src/analytics; sudo R < dependencies.R --no-save
	sudo easy_install BeautifulSoup
	sudo easy_install nltk
	sudo easy_install inflect
	sudo easy_install html2text
	sudo easy_install gdata
	sudo easy_install jinja2
	sudo easy_install mako
	sudo easy_install asq
	python -m nltk.downloader all

bootstrap:
	cd src; python bootstrap.py

# Run mining scripts
mine:
	cd src; make mine

# Run analytics scripts
analyze:
	cd src; make analyze

# Copies post processed data from cache
from-cache:
	cd src; make from-cache

# Copies post-processed data, required for analytics, to cache
to-cache:
	cd src; make to-cache


# Run backlinking scripts
backlink:
	cd src; make backlink

coverageTables:
	cd src make coverageTables

nonProfileFrequencies:
	cd src; make nonProfileFrequencies

# Clean it all
clean:
	cd data/allbooks; rm -f *.tex *.csv *.json *.png *.html
	for b in ${ALL_BOOKS}; do \
		cd data/perbook/"$$b"; rm -rf contents *.tex *.csv *.json *.png *.html ;\
		cd ../../.. ;\
	done
