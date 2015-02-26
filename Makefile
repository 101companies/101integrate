# Key for Google Docs
INDEXKEY = 0AtMdJdyllDEfdC1YMHE5NmNzNEc3bGx3aV9NbDc2V0E

# Please, read the README.md.
nope:
	@echo Please, read the README.md.
	
	
run:
ifndef LOGGING
	$(MAKE) download-books
	$(MAKE) mine
	$(MAKE) from-cache
	$(MAKE) analyze
	$(MAKE) backlink
	$(MAKE) integrate
else
ifeq ($(LOGGING),ON)
	mkdir -p logs
	$(MAKE) download-books | tee logs/downloadBooks.log
	$(MAKE) mine           | tee logs/mine.log
	$(MAKE) from-cache     | tee logs/fromCache.log
	$(MAKE) analyze        | tee logs/analyze.log
	$(MAKE) backlink       | tee logs/backlink.log
	$(MAKE) integrate      | tee logs/integrate.log
else
	$(MAKE) download-books
	$(MAKE) mine
	$(MAKE) from-cache
	$(MAKE) analyze
	$(MAKE) backlink
	$(MAKE) integrate
endif
endif

# Download books that are available online
download-books:
ifndef BOOKS
ifndef BOOK
	cd src/mining; python bookDownloader.py all
else
	cd src/mining; python bookDownloader.py $(BOOK)
endif
else
	cd src/mining; python bookDownloader.py $(BOOKS)
endif
	$(MAKE) bootstrap
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


# Run backlinking scripts
backlink:
	cd src; $(MAKE) backlink

coverageTables:
	cd src $(MAKE) coverageTables

nonProfileFrequencies:
	cd src; $(MAKE) nonProfileFrequencies
	
integrate:
	cd src; $(MAKE) integrate

# Clean it all
clean:
	cd src; $(MAKE) clean
