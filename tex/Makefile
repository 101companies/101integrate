all: report.pdf

%.pdf: %.tex Makefile *.tex
	-pdflatex $*
	-pdflatex $*

clean:
	rm -f *.pdf
	rm -f *.aux
	rm -f *.dvi
	rm -f *.log
	rm -f *.bbl
	rm -f *.blg
	rm -f *.zip


