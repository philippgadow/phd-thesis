wjets:
	lualatex wjets.tex
	rm *.aux *.log
	../scripts/convertToEps.sh wjets
	../scripts/convertEpsToPng.sh
	okular wjets.eps

clean:
	rm *.pdf *.aux *.log *.eps

.PHONY: wjets clean
