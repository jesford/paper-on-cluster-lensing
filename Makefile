pdf: clusterlensing.pdf
	
clusterlensing.pdf: clusterlensing.tex
	pdflatex clusterlensing
	bibtex clusterlensing
	pdflatex clusterlensing
	pdflatex clusterlensing

clean:
		rm -f *.log
		rm -f *.aux
		rm -f *.gz
		rm -f *.bbl
		rm -f *.blg
		rm -f *.brf
		rm -f *.dvi
		rm -f *.out
		rm -f *.snippets
		rm -f clusterlensingNotes.bib
		#rm -f clusterlensing.pdf
		ls -ltr
