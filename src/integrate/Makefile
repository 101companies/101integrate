include ../Makefile.vars
DATAFOLDER = ../../data/

coverageTables:
	python termsCoverage.py $(DATAFOLDER) allbooks/

nonProfileFrequencies:
	for b in ${LINKED_BOOKS}; do \
		python nonProfileFrequencies.py ../../data/perbook/ "$$b" $(foreach r,$(LINKED_BOOKS), $(r)); \
	done
