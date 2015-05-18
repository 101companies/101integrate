include Makefile.vars
include ../Makefile.vars

CACHE_FILES = frequenciesMerged.csv frequenciesDistributionMerged.csv frequencies.json

# Please, read the README.md.
nope:
	@echo Please, read the README.md.

# Run mining scripts
mine:
	cd mining; $(MAKE) mine LOGGING=$(LOGGING)

# Run analytics scripts
analyze:
	$(MAKE) from-cache
	cd analytics; $(MAKE) analyze LOGGING=$(LOGGING)

# Copies post processed data from cache
from-cache:
	for b in ${NON_LINKED_BOOKS}; do \
		for f in ${CACHE_FILES}; do \
			cp ../data/perbook/"$$b"/cache/"$$f"  ../data/perbook/"$$b"/ ;\
		done \
	done

# Copies post-processed data, required for analytics, to cache
to-cache:
	for b in ${LINKED_BOOKS}; do \
		for f in ${CACHE_FILES}; do \
			cp ../data/perbook/"$$b"/"$$f"  ../data/perbook/"$$b"/cache ;\
		done \
	done

#runs integration-scripts
integrate:
	cd integrate; $(MAKE) integrate	LOGGING=$(LOGGING)

# Run backlinking scripts
backlink:
	cd mining; $(MAKE) backlink LOGGING=$(LOGGING)

coverageTables:
	cd integrate; $(MAKE) coverageTables

nonProfileFrequencies:
	cd integrate; $(MAKE) nonProfileFrequencies
	
# Clean it all
clean:
	cd ../; rm -rf logs/
	cd ../data/allbooks; rm -f *.tex *.csv *.json *.png *.html
	cd ..; for b in ${ALL_BOOKS}; do \
			cd data/perbook/"$$b"; rm -rf contents *.tex *.csv *.json *.png *.html ; \
			cd ../../.. ;\
			rm -rf data/perbook/"$$b"/contents; \
	done
