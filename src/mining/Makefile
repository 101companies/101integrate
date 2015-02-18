include ../Makefile.vars


DATAFOLDER = ../../data/

#HTML2TXT=../../bin/html2text 

mine:
	$(MAKE) cleanindecies
	$(MAKE) mergeindecies
	$(MAKE) frequencies
	$(MAKE) mergedfrequencies
	
backlink:
	$(MAKE) backlinksMappings
	$(MAKE) mergeBacklinkMappings
	$(MAKE) mergeMappings

# Clean online books once after download
cleanOnlineBooks:
	for b in ${LINKED_BOOKS}; do \
		for h in ../../data/perbook/"$$b"/contents/*; do \
			 html2text "$$h" --ignore-links --ignore-images| tee "$$h".txt; \
			rm "$$h"; \
		done \
	done

cleanindecies:
	for b in ${LINKED_BOOKS}; do \
		python merge.py $(DATAFOLDER)/ perbook/ "$$b" Index.csv perbook/"$$b"/CleanIndex.csv perbook/"$$b"/metaindex.json 30 nocrosscut; \
	done

mergeindecies:
	python merge.py $(DATAFOLDER) /perbook/ $(foreach r,$(LINKED_BOOKS), $(r)) Index.csv allbooks/Index.csv allbooks/metaindex.json 30 allbooks/crosscuts.csv

frequencies:
	for b in ${LINKED_BOOKS}; do \
		python frequencies.py "$$b" $(DATAFOLDER) perbook/"$$b"/ perbook/"$$b"/ CleanIndex.csv metadata/chapters.json contents/ metaindex.json nonmerged; \
	done

mergedfrequencies:
	for b in ${LINKED_BOOKS}; do \
		python frequencies.py "$$b" $(DATAFOLDER) perbook/"$$b"/ allbooks/ Index.csv metadata/chapters.json contents/ metaindex.json merged; \
	done

backlinksMappings:
	for b in ${LINKED_BOOKS}; do \
		python backlinksMapper.py "$$b" ../../data/perbook/ frequenciesDistributionDeepMerged.json contents/ 5; \
	done

mergeBacklinkMappings:
	python mergeBacklinks.py $(DATAFOLDER) perbook/ $(foreach r,$(LINKED_BOOKS), $(r)) allbooks/

mergeMappings:
	python mergeMappings.py $(DATAFOLDER) perbook/ $(foreach r,$(ALL_BOOKS), $(r)) allbooks/

deployBacklinks:
	scp  ../../data/allbooks/backlinks.json ../../data/allbooks/mapping.json worker@black42.uni-koblenz.de:~/101worker/services/termResources/

termCoverage:
	python termCoverage.py $(DATAFOLDER)/allbooks/
	
indexBlacklist:
	for b in ${LINKED_BOOKS}; do \
		python csvDiff.py $(DATAFOLDER)/perbook/"$$b"/IndexGen.csv $(DATAFOLDER)/perbook/"$$b"/Index.csv del csv $(DATAFOLDER)/perbook/"$$b"/indexBlacklist.csv
	done