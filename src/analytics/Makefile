BOOKS = LYAH RWH Craft PIH

analyze:
	make frequencies
	make popular
	make move

prepare:
	R < dependencies.R --no-save

frequencies:	
	for b in ${BOOKS}; do \
		R < frequencies.R --no-save --args ""$$b""; \
	done

popular:	
	R < buildPopularTermsTable.R --no-save
	R < buildPopularScatteredTermsTable.R --no-save
	R < rank.R --no-save
move:
	mv Craft/Craft.numbers ../../data/perbook/Craft/chapterProfile.numbers.tex
	mv Craft/Craft.visual ../../data/perbook/Craft/chapterProfile.visual.tex

	mv LYAH/LYAH.numbers ../../data/perbook/LYAH/chapterProfile.numbers.tex
	mv LYAH/LYAH.visual ../../data/perbook/LYAH/chapterProfile.visual.tex

	mv PIH/PIH.numbers ../../data/perbook/PIH/chapterProfile.numbers.tex
	mv PIH/PIH.visual ../../data/perbook/PIH/chapterProfile.visual.tex

	mv RWH/RWH.numbers ../../data/perbook/RWH/chapterProfile.numbers.tex
	mv RWH/RWH.visual ../../data/perbook/RWH/chapterProfile.visual.tex

	mv Craft/topFrequency.tex ../../data/perbook/Craft/topFrequency.tex
	mv LYAH/topFrequency.tex ../../data/perbook/LYAH/topFrequency.tex
	mv RWH/topFrequency.tex ../../data/perbook/RWH/topFrequency.tex
	mv PIH/topFrequency.tex ../../data/perbook/PIH/topFrequency.tex

	mv RWH/topScattered.tex ../../data/perbook/RWH/topScattered.tex
	mv LYAH/topScattered.tex ../../data/perbook/LYAH/topScattered.tex
	mv Craft/topScattered.tex ../../data/perbook/Craft/topScattered.tex
	mv PIH/topScattered.tex ../../data/perbook/PIH/topScattered.tex

	mv unionTopFrequencies.tex ../../data/allbooks/
	mv unionTopFrequencies.csv ../../data/allbooks/
	mv unionTopFrequenciesVisual.tex ../../data/allbooks/
	
	mv unionTopScatterness.tex ../../data/allbooks/
	mv unionTopScatterness.csv ../../data/allbooks/
	mv unionTopScatternessVisual.tex ../../data/allbooks/

	mv ranks.tex ../../data/allbooks/	
