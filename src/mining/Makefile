include ../Makefile.vars

ONLINEBOOKS = RWH LYAH
DATAFOLDER = ../../data/

mine:
	make cleanindecies
	make mergeindecies
	make frequencies
	make mergedfrequencies

backlink:
	make backlinksMappings
	make mergeBacklinkMappings
	make mergeMappings

# Clean online books once after download
cleanOnlineBooks:
	for b in ${ONLINEBOOKS}; do \
		for h in ../../data/perbook/"$$b"/contents/*; do \
			html2text "$$h" --ignore-links --ignore-images| tee "$$h".txt; \
			rm "$$h"; \
		done \
	done

cleanindecies:
	for b in ${BOOKS}; do \
		python merge.py $(DATAFOLDER)/ perbook/ "$$b" cache/Index.csv perbook/"$$b"/CleanIndex.csv perbook/"$$b"/metaindex.json 30 nocrosscut; \
	done

mergeindecies:
	python merge.py $(DATAFOLDER) /perbook/ $(foreach r,$(BOOKS), $(r)) cache/Index.csv allbooks/Index.csv allbooks/metaindex.json 30 allbooks/crosscuts.csv

frequencies:
	for b in ${BOOKS}; do \
		python frequencies.py "$$b" $(DATAFOLDER) perbook/"$$b"/ perbook/"$$b"/ CleanIndex.csv metadata/chapters.json contents/ metaindex.json nonmerged; \
	done

mergedfrequencies:
	for b in ${BOOKS}; do \
		python frequencies.py "$$b" $(DATAFOLDER) perbook/"$$b"/ allbooks/ Index.csv metadata/chapters.json contents/ metaindex.json merged; \
	done

backlinksMappings:
	for b in ${BOOKS}; do \
		python backlinksMapper.py "$$b" ../../data/perbook/ frequenciesDistributionDeepMerged.json contents/ 5; \
	done

mergeBacklinkMappings:
	python mergeBacklinks.py $(DATAFOLDER) perbook/ $(foreach r,$(BOOKS), $(r)) allbooks/

mergeMappings:
	python mergeMappings.py $(DATAFOLDER) perbook/ $(foreach r,$(BOOKS), $(r)) allbooks/

deployBacklinks:
	scp  ../../data/allbooks/backlinks.json ../../data/allbooks/mapping.json worker@black42.uni-koblenz.de:~/101worker/services/termResources/

make termCoverage:
	python termCoverage.py $(DATAFOLDER)/allbooks/
