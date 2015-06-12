include Makefile.vars

#Programs
PYTHON_PACKAGE_INSTALLER = pip install --upgrade

# Key for Google Docs
INDEXKEY = 0AtMdJdyllDEfdC1YMHE5NmNzNEc3bGx3aV9NbDc2V0E

# Please, read the README.md.
nope:
	@echo Please, read the README.md.
	
#Complete Integration of resources	
run:
ifeq ($(LOGGING),ON)
	mkdir -p logs
	cp src/config/pythonLoggingDebug.conf src/config/pythonLogging.conf
	$(MAKE) download-books BOOKS=$(BOOKS) 2>&1 | tee logs/downloadBooks.log
	$(MAKE) mine           LOGGING=ON
	$(MAKE) from-cache     2>&1	| tee logs/fromCache.log
	$(MAKE) analyze        LOGGING=ON
	$(MAKE) backlink       LOGGING=ON
	$(MAKE) integrate      LOGGING=ON
else
	cp src/config/pythonLoggingRun.conf src/config/pythonLogging.conf
	$(MAKE) download-books BOOKS=$(BOOKS)
	$(MAKE) mine
	$(MAKE) from-cache
	$(MAKE) analyze
	$(MAKE) backlink
	$(MAKE) integrate
endif



# Download books that are available online
download-books:
ifndef BOOKS
	cd src/mining; $(PYTHON) bookDownloader.py all
	$(MAKE) bootstrap
else
	cd src/mining; $(PYTHON) bookDownloader.py $(BOOKS)
	$(MAKE) bootstrap BOOKS=$(BOOKS)
endif
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
	sudo $(PYTHON_PACKAGE_INSTALLER) BeautifulSoup
	sudo $(PYTHON_PACKAGE_INSTALLER) numpy
	sudo $(PYTHON_PACKAGE_INSTALLER) nltk
	sudo $(PYTHON_PACKAGE_INSTALLER) inflect
	sudo $(PYTHON_PACKAGE_INSTALLER) html2text
	sudo $(PYTHON_PACKAGE_INSTALLER) gdata
	sudo $(PYTHON_PACKAGE_INSTALLER) jinja2
	sudo $(PYTHON_PACKAGE_INSTALLER) mako
	sudo $(PYTHON_PACKAGE_INSTALLER) asq
	sudo $(PYTHON_PACKAGE_INSTALLER) simplejson
	sudo $(PYTHON_PACKAGE_INSTALLER) stringtemplate3 #Still needs antlr, but not available on pypi
	sudo $(PYTHON_PACKAGE_INSTALLER) sortedcontainers
	sudo $(PYTHON_PACKAGE_INSTALLER) logging
	$(PYTHON) -m nltk.downloader all
	cd src; touch Makefile.vars
	cd src/analytics; $(MAKE) prepare

bootstrap:
ifndef BOOKS
	cd src; $(PYTHON) bootstrap.py
else
	cd src; $(PYTHON) bootstrap.py $(BOOKS)
endif

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
	cd src; $(MAKE) coverageTables

nonProfileFrequencies:
	cd src; $(MAKE) nonProfileFrequencies
	
integrate:
	cd src; $(MAKE) integrate LOGGING=$(LOGGING)

# Clean it all
clean:
	cd src; $(MAKE) clean
