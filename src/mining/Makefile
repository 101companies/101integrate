include ../Makefile.vars
include ../../Makefile.vars


DATAFOLDER := ../../data
MLOGFOLDER := ../../logs/mining
BLOGFOLDER := ../../logs/backlink

#HTML2TXT=../../bin/html2text 
HTML2TXT := $(subst html2text: ,,$(shell whereis html2text))

mine:
ifeq ($(LOGGING),ON)
	mkdir -p  $(MLOGFOLDER)
ifneq (,$(strip $(shell diff ../Makefile.vars ../last.vars)))
	$(MAKE) rankTerms	2>&1	|	tee $(MLOGFOLDER)/rankTerms.log
endif
	$(MAKE) cleanindecies		2>&1	| tee $(MLOGFOLDER)/cleanindecies.log
	$(MAKE) mergeindecies		2>&1	| tee $(MLOGFOLDER)/mergeindecies.log
	$(MAKE) frequencies		2>&1	| tee $(MLOGFOLDER)/frequencies.log
	$(MAKE) mergedfrequencies	2>&1	| tee $(MLOGFOLDER)/mergedfrequencies.log
else
ifneq (,$(strip $(shell diff ../Makefile.vars ../last.vars)))
	$(MAKE) rankTerms
endif
	$(MAKE) cleanindecies
	$(MAKE) mergeindecies
	$(MAKE) frequencies
	$(MAKE) mergedfrequencies
endif
	
backlink:
ifeq ($(LOGGING),ON)
	mkdir -p  $(BLOGFOLDER)/
	$(MAKE) backlinksMappings	2>&1	| tee $(BLOGFOLDER)/backlinksMappings.log
	$(MAKE) mergeBacklinkMappings	2>&1	| tee $(BLOGFOLDER)/mergeBacklinkMappings.log
	$(MAKE) mergeMappings		2>&1	| tee $(BLOGFOLDER)/mergeMappings.log
else
	$(MAKE) backlinksMappings
	$(MAKE) mergeBacklinkMappings
	$(MAKE) mergeMappings
endif

# Clean online books once after download
cleanOnlineBooks:
	for b in ${LINKED_BOOKS}; do \
		echo "$$b" ;\
		for h in ../../data/perbook/"$$b"/contents/*; do \
			$(HTML2TXT) "$$h" --ignore-links --ignore-images > "$$h".temp; \
			rm "$$h"; \
			mv "$$h".temp "$$h" ;\
		done \
	done


cleanindecies:
	for b in ${LINKED_BOOKS}; do \
		$(PYTHON) merge.py $(DATAFOLDER)/ perbook/ "$$b" cache/Index.csv perbook/"$$b"/CleanIndex.csv perbook/"$$b"/metaindex.json 50 nocrosscut; \
	done

mergeindecies:
	$(PYTHON) merge.py $(DATAFOLDER)/ /perbook/ $(foreach r,$(LINKED_BOOKS), $(r)) cache/Index.csv allbooks/Index.csv allbooks/metaindex.json 50 allbooks/crosscuts.csv

frequencies:
	for b in ${LINKED_BOOKS}; do \
		$(PYTHON) frequencies.py "$$b" $(DATAFOLDER)/ perbook/"$$b"/ perbook/"$$b"/ CleanIndex.csv metadata/chapters.json contents/ metaindex.json nonmerged; \
	done

mergedfrequencies:
	for b in ${LINKED_BOOKS}; do \
		$(PYTHON) frequencies.py "$$b" $(DATAFOLDER)/ perbook/"$$b"/ allbooks/ Index.csv metadata/chapters.json contents/ metaindex.json merged; \
	done

backlinksMappings:
	for b in ${LINKED_BOOKS}; do \
		$(PYTHON) backlinksMapper.py "$$b" ../../data/perbook/ frequenciesDistributionDeepMerged.json 5; \
	done

mergeBacklinkMappings:
	$(PYTHON) mergeBacklinks.py $(DATAFOLDER)/ perbook/ $(foreach r,$(LINKED_BOOKS), $(r)) allbooks/

mergeMappings:
	$(PYTHON) mergeMappings.py $(DATAFOLDER)/ perbook/ $(foreach r,$(ALL_BOOKS), $(r)) allbooks/

deployBacklinks:
	scp  ../../data/allbooks/backlinks.json ../../data/allbooks/mapping.json worker@black42.uni-koblenz.de:~/101worker/services/termResources/

termCoverage:
	$(PYTHON) termCoverage.py $(DATAFOLDER)/allbooks/
	
rankTerms:
	$(PYTHON) ranker.py $(DATAFOLDER)/perbook/ /cache/Index.csv $(foreach r,$(ALL_BOOKS), $(r)) $(DATAFOLDER)/allbooks/cache/rank.csv
	
indexBlacklist:
	for b in ${LINKED_BOOKS}; do \
		$(PYTHON) ../misc/csvDiff.py $(DATAFOLDER)/perbook/"$$b"/IndexGen.csv $(DATAFOLDER)/perbook/"$$b"/cache/Index.csv del csv $(DATAFOLDER)/perbook/"$$b"/cache/indexBlacklist.csv ; \
	done
	
