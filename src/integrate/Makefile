include ../Makefile.vars
DATAFOLDER = ../../data/

integrate:
	make coverageTables
	make uniqueTerms
	make nonProfileFrequencies

make coverageTables:
	python termsCoverage.py $(DATAFOLDER) allbooks/

nonProfileFrequencies:
	for b in ${ALL_BOOKS}; do \
		python nonProfileFrequencies.py $(DATAFOLDER)/perbook/ "$$b" $(foreach r,$(LINKED_BOOKS), $(r)); \
	done

make uniqueTerms:
	python uniqueTerms.py
