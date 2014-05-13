include ../Makefile.vars

analyze:
	$(MAKE) frequencies
	$(MAKE) popular
	$(MAKE) tex

frequencies:	
	for b in ${ALL_BOOKS}; do \
		R < frequencies.R --no-save --args ""$$b""; \
	done

popular:	
	R < buildPopularTermsTable.R --no-save
	R < buildPopularScatteredTermsTable.R --no-save
	R < rank.R --no-save

tex:
	for b in ${ALL_BOOKS}; do \
		./csv2tex.py --input ../../data/perbook/"$$b"/chapterProfile.numbers.csv --template "tabular_template_with_hlines.tex" ; \
		./csv2tex.py --input ../../data/perbook/"$$b"/chapterProfile.visual.csv --template "tabular_template_with_hlines.tex" ; \
	done
	#mv Craft/Craft.numbers ../../data/perbook/Craft/chapterProfile.numbers.tex
	#mv Craft/Craft.visual ../../data/perbook/Craft/chapterProfile.visual.tex

	#mv LYAH/LYAH.numbers ../../data/perbook/LYAH/chapterProfile.numbers.tex
	#mv LYAH/LYAH.visual ../../data/perbook/LYAH/chapterProfile.visual.tex

	#mv PIH/PIH.numbers ../../data/perbook/PIH/chapterProfile.numbers.tex
	#mv PIH/PIH.visual ../../data/perbook/PIH/chapterProfile.visual.tex

	#mv RWH/RWH.numbers ../../data/perbook/RWH/chapterProfile.numbers.tex
	#mv RWH/RWH.visual ../../data/perbook/RWH/chapterProfile.visual.tex

	#mv Craft/topFrequency.tex ../../data/perbook/Craft/topFrequency.tex
	#mv LYAH/topFrequency.tex ../../data/perbook/LYAH/topFrequency.tex
	#mv RWH/topFrequency.tex ../../data/perbook/RWH/topFrequency.tex
	#mv PIH/topFrequency.tex ../../data/perbook/PIH/topFrequency.tex

	for b in ${ALL_BOOKS}; do \
		./csv2tex.py --input ../../data/perbook/"$$b"/topFrequency.csv --template "tabular_template.tex" ; \
	done

	for b in ${ALL_BOOKS}; do \
		./csv2tex.py --input ../../data/perbook/"$$b"/topScattered.csv --template "tabular_template.tex" ; \
	done

	#mv RWH/topScattered.tex ../../data/perbook/RWH/topScattered.tex
	#mv LYAH/topScattered.tex ../../data/perbook/LYAH/topScattered.tex
	#mv Craft/topScattered.tex ../../data/perbook/Craft/topScattered.tex
	#mv PIH/topScattered.tex ../../data/perbook/PIH/topScattered.tex

	./csv2tex.py --input ../../data/allbooks/unionTopFrequencies.csv --template "tabular_template.tex" #--caption "Union Top Frequencies" --label "t:union"
	./csv2tex.py --input ../../data/allbooks/unionTopFrequenciesVisual.csv --template "tabular_template.tex" #--caption "Union Top Frequencies Visual" --label "t:unionVisual"

	#mv unionTopFrequencies.csv ../../data/allbooks/
	#mv unionTopFrequenciesVisual.tex ../../data/allbooks/

	./csv2tex.py --input ../../data/allbooks/unionTopScatternessVisual.csv --template "tabular_template.tex" #--caption "Union Top Frequencies" --label "t:union"

	#mv unionTopScatterness.csv ../../data/allbooks/
	#mv unionTopScatternessVisual.tex ../../data/allbooks/

	#mv ranks.tex ../../data/allbooks/	
	./csv2tex.py --input ../../data/allbooks/rank.csv --template "tabular_template.tex"
