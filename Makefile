include Makefile.vars

# Please, read the README.md.
nope:
	@echo Please, read the README.md.
	
	
run:
	$(MAKE) download-books
	$(MAKE) bootstrap
	$(MAKE) mine
	$(MAKE) from-cache
	$(MAKE) analyze
	$(MAKE) backlink
	$(MAKE) integrate

# Download books that are available online
download-books:
ONLINEBOOKS = 
ifneq (,$(findstring haskell,$(BOOKS)))
	ONLINEBOOKS = $(HASKELLBOOKSONLINE)
else
	ONLINEBOOKS = $(ALLBOOKS)
endif
$(MAKE) download-books-helper ONLINEBOOKS=$(ONLINEBOOKS)

#help-function "Real Downloader"
download-books-helper:
	for b in ${ONLINEBOOKS}; do \
		mkdir -p data/perbook/"$$b"/contents; \
		cd src/mining; python crawler.py "$$b" ../../data/perbook/;\
		cd ../..;\
	done
	cd src/mining; $(MAKE) cleanOnlineBooks

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
	cd src; $(MAKE) mine

# Run analytics scripts
analyze:
	cd src; $(MAKE) analyze

# Copies post processed data from cache
from-cache:
	cd src; $(MAKE) from-cache

# Copies post-processed data, required for analytics, to cache
to-cache:
	cd src; $(MAKE) to-cache
	
#runs integration-scripts
integrate:
	cd src; $(MAKE) integrate

# Run backlinking scripts
backlink:
	cd src; $(MAKE) backlink

coverageTables:
	cd src; $(MAKE) coverageTables

nonProfileFrequencies:
	cd src; $(MAKE) nonProfileFrequencies

# Clean it all
clean:
	cd src; $(MAKE) clean
