include ../Makefile.vars


DATAFOLDER = ../../data/

#HTML2TXT=../../bin/html2text 

mine:
	$(MAKE) cleanindecies
	$(MAKE) mergeindecies
	$(MAKE) frequencies
	$(MAKE) mergedfrequencies
	$(MAKE) move

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
		python merge.py $(DATAFOLDER)/ perbook/ "$$b" cache/Index.csv perbook/"$$b"/cache/CleanIndex.csv perbook/"$$b"/cache/metaindex.json 30 nocrosscut; \
	done

mergeindecies:
	python merge.py $(DATAFOLDER) /perbook/ $(foreach r,$(LINKED_BOOKS), $(r)) cache/Index.csv allbooks/Index.csv allbooks/metaindex.json 30 allbooks/crosscuts.csv

frequencies:
	for b in ${LINKED_BOOKS}; do \
		python frequencies.py "$$b" $(DATAFOLDER) perbook/"$$b"/ perbook/"$$b"/cache/ CleanIndex.csv metadata/chapters.json contents/ metaindex.json nonmerged; \
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

move:
	for b in ${LINKED_BOOKS}; do \
		mv -f ../../data/perbook/"$$b"/frequencies.json ../../data/perbook/"$$b"/cache/frequencies.json; \
		mv -f ../../data/perbook/"$$b"/frequencies.csv ../../data/perbook/"$$b"/cache/frequencies.csv; \
		mv -f ../../data/perbook/"$$b"/frequenciesDistribution.json ../../data/perbook/"$$b"/cache/frequenciesDistribution.json; \
		mv -f ../../data/perbook/"$$b"/frequenciesDistribution.csv ../../data/perbook/"$$b"/cache/frequenciesDistribution.csv; \
		mv -f ../../data/perbook/"$$b"/frequenciesDistributionDeepMerged.json ../../data/perbook/"$$b"/cache/frequenciesDistributionDeepMerged.json; \
		mv -f ../../data/perbook/"$$b"/frequenciesMerged.json ../../data/perbook/"$$b"/cache/frequenciesMerged.json; \
		mv -f ../../data/perbook/"$$b"/frequenciesMerged.csv ../../data/perbook/"$$b"/cache/frequenciesMerged.csv; \
		mv -f ../../data/perbook/"$$b"/frequenciesDistributionDeep.json ../../data/perbook/"$$b"/cache/frequenciesDistributionDeep.json; \
		mv -f ../../data/perbook/"$$b"/frequenciesDistributionMerged.json ../../data/perbook/"$$b"/cache/frequenciesDistributionMerged.json; \
		mv -f ../../data/perbook/"$$b"/frequenciesDistributionMerged.csv ../../data/perbook/"$$b"/cache/frequenciesDistributionMerged.csv; \
	done \
