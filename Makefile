include Makefile.vars

# Key for Google Docs
INDEXKEY = 0AtMdJdyllDEfdC1YMHE5NmNzNEc3bGx3aV9NbDc2V0E

# Please, read the README.md.
nope:
	@echo Please, read the README.md.
	
	
run:
ifeq ($(LOGGING),ON)
	mkdir -p logs
	$(MAKE) download-books 2>&1	| tee logs/downloadBooks.log
	$(MAKE) mine           LOGGING=ON
	$(MAKE) from-cache     2>&1	| tee logs/fromCache.log
	$(MAKE) analyze        LOGGING=ON
	$(MAKE) backlink       LOGGING=ON
	$(MAKE) integrate      LOGGING=ON
else
	$(MAKE) download-books
	$(MAKE) mine
	$(MAKE) from-cache
	$(MAKE) analyze
	$(MAKE) backlink
	$(MAKE) integrate
endif

# Download books that are available online
download-books:
ifndef BOOKS
ifndef BOOK
	cd src/mining; $(PYTHON) bookDownloader.py all
else
	cd src/mining; $(PYTHON) bookDownloader.py $(BOOK)
endif
else
	cd src/mining; $(PYTHON) bookDownloader.py $(BOOKS)
endif
	$(MAKE) bootstrap
	cd src/mining; $(MAKE) cleanOnlineBooks

# Optionally link offline books, as explained in the README.md
link-books:
	cd data/perbook/PIH; ln -s ~/Dropbox/haskellbooks/clean/PIH/contents
	cd data/perbook/Craft; ln -s ~/Dropbox/haskellbooks/clean/Craft/contents

# Optionally renew google doc data
download-googledocs:
	$(PYTHON) src/misc/downloader.py $(INDEXKEY) data/perbook/ LYAH RWH Craft PIH

# Get Python and R tools
download-deps:
	cd src/analytics; sudo R < dependencies.R --no-save
	sudo easy_install BeautifulSoup
	sudo easy_install numpy
	sudo easy_install nltk
	sudo easy_install inflect
	sudo easy_install html2text
	sudo easy_install gdata
	sudo easy_install jinja2
	sudo easy_install mako
	sudo easy_install asq
	sudo easy_install simplejson
	sudo easy_install sortedcontainers
	$(PYTHON) -m nltk.downloader all

bootstrap:
	cd src; $(PYTHON) bootstrap.py

# Run mining scripts
mine:
	cd src; $(MAKE) mine LOGGING=$(LOGGING)

# Run analytics scripts
analyze:
	cd src; $(MAKE) analyze LOGGING=$(LOGGING)

# Copies post processed data from cache
from-cache:
	cd src; $(MAKE) from-cache

# Copies post-processed data, required for analytics, to cache
to-cache:
	cd src; $(MAKE) to-cache


# Run backlinking scripts
backlink:
	cd src; $(MAKE) backlink LOGGING=$(LOGGING)

coverageTables:
	cd src $(MAKE) coverageTables

nonProfileFrequencies:
	cd src; $(MAKE) nonProfileFrequencies
	
integrate:
	cd src; $(MAKE) integrate LOGGING=$(LOGGING)

# Clean it all
clean:
	cd src; $(MAKE) clean
