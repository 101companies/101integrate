include Makefile.vars


# Please, read the README.md.
nope:
	@echo Please, read the README.md.

# Run mining scripts
mine:
	cd mining; make mine

# Run analytics scripts
analyze:
	make from-cache
	cd analytics; make analyze

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

# Run backlinking scripts
backlink:
	cd mining; make backlink

coverageTables:
	cd integrate; make coverageTables

nonProfileFrequencies:
	cd integrate; make nonProfileFrequencies
