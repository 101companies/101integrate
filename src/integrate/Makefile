include ../Makefile.vars
DATAFOLDER = ../../data

integrate:
	$(MAKE) coverageTables
	$(MAKE) uniqueTerms
	$(MAKE) nonProfileFrequencies

coverageTables:
	python termsCoverage.py $(DATAFOLDER) allbooks/

nonProfileFrequencies:
	for b in ${ALL_BOOKS}; do \
		python nonProfileFrequencies.py $(DATAFOLDER)/ allbooks/cache/ /perbook/ "$$b" $(foreach r,$(LINKED_BOOKS), $(r)); \
	done

uniqueTerms:
	python uniqueTerms.py
