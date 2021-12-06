zjets:
	lualatex zjets.tex
	rm *.aux *.log
	../scripts/convertToEps.sh zjets
	../scripts/convertEpsToPng.sh
	okular zjets.eps

clean:
	rm *.pdf *.aux *.log *.eps

.PHONY: zjets clean
