include ../Makefile.vars
DATAFOLDER = ../../data

integrate:
ifeq ($(LOGGING),ON)
	mkdir -p ../../logs/integrate
	$(MAKE) coverageTables		| tee ../../logs/integrate/coverageTables.log
	$(MAKE) uniqueTerms		| tee ../../logs/integrate/uniqueTerms.log
	$(MAKE) nonProfileFrequencies	| tee ../../logs/integrate/nonProfileFrequencies.log
else
	$(MAKE) coverageTables
	$(MAKE) uniqueTerms
	$(MAKE) nonProfileFrequencies
endif

coverageTables:
	python termsCoverage.py $(DATAFOLDER) allbooks/

nonProfileFrequencies:
	for b in ${ALL_BOOKS}; do \
		python nonProfileFrequencies.py $(DATAFOLDER)/ allbooks/cache/ /perbook/ "$$b" $(foreach r,$(LINKED_BOOKS), $(r)); \
	done

uniqueTerms:
	python uniqueTerms.py
