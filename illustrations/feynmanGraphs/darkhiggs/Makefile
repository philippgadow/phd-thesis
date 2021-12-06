darkhiggs1:
	lualatex darkhiggs1.tex
	rm *.aux *.log
	../scripts/convertToEps.sh darkhiggs1
	../scripts/convertEpsToPng.sh

darkhiggs2:
	lualatex darkhiggs2.tex
	rm *.aux *.log
	../scripts/convertToEps.sh darkhiggs2
	../scripts/convertEpsToPng.sh

clean:
	rm *.pdf *.aux *.log *.eps

.PHONY: darkhiggs1 darkhiggs2
