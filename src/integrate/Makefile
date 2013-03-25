DATAFOLDER = ../../data/

integrate:
	make coverageTables
	make uniqueTerms

make coverageTables:
	python termsCoverage.py $(DATAFOLDER) allbooks/

make uniqueTerms:
	python uniqueTerms.py
