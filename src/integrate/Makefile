include ../Makefile.vars
include ../../Makefile.vars
DATAFOLDER = ../../data

integrate:
ifeq ($(LOGGING),ON)
	mkdir -p ../../logs/integrate
	$(MAKE) coverageTables		2>&1	| tee ../../logs/integrate/coverageTables.log
	$(MAKE) uniqueTerms		2>&1	| tee ../../logs/integrate/uniqueTerms.log
	$(MAKE) nonProfileFrequencies	2>&1	| tee ../../logs/integrate/nonProfileFrequencies.log
else
	$(MAKE) coverageTables
	$(MAKE) uniqueTerms
	$(MAKE) nonProfileFrequencies
endif

coverageTables:
	$(PYTHON) termsCoverage.py $(DATAFOLDER) allbooks/

nonProfileFrequencies:
	for b in ${ALL_BOOKS}; do \
		$(PYTHON) nonProfileFrequencies.py $(DATAFOLDER)/ allbooks/cache/ /perbook/ "$$b" $(foreach r,$(LINKED_BOOKS), $(r)); \
	done

uniqueTerms:
	$(PYTHON) uniqueTerms.py
