default: paper
	
paper:
	pdflatex  -shell-escape clusterlensing
	bibtex clusterlensing
	pdflatex  -shell-escape clusterlensing
	pdflatex  -shell-escape clusterlensing
	pdflatex  -shell-escape clusterlensing

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
		rm -f data/*eps-converted-to.pdf
		ls -ltr
