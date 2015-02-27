include Makefile.vars


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
		cp ../data/perbook/$$b/cache/frequenciesMerged.csv  ../data/perbook/"$$b"/ ;\
		cp ../data/perbook/$$b/cache/frequenciesDistributionMerged.csv  ../data/perbook/"$$b"/ ;\
		cp ../data/perbook/$$b/cache/frequencies.json ../data/perbook/"$$b"/ ;\
	done

# Copies post-processed data, required for analytics, to cache
to-cache:
	for b in ${LINKED_BOOKS}; do \
		cp ../data/perbook/$$b/frequenciesMerged.csv  ../data/perbook/"$$b"/cache ;\
		cp ../data/perbook/$$b/frequenciesDistributionMerged.csv  ../data/perbook/"$$b"/cache ;\
		cp ../data/perbook/$$b/frequencies.json  ../data/perbook/"$$b"/cache ;\
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
	cd ../data/allbooks; rm -f *.tex *.csv *.json *.png *.html
	cd ..; for b in ${ALL_BOOKS}; do \
			cd data/perbook/"$$b"; rm -rf contents *.tex *.csv *.json *.png *.html ; \
			cd ../../.. ;\
			rm -rf data/perbook/"$$b"/contents; \
	done
