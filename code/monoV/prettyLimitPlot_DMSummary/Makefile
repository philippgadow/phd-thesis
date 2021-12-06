.PHONY: makePlot

makePlot:
	mkdir -p plots
	python3 pretty1DLimitPlot.py data/resolvedonly_obs_PS2HDM_limits.txt -m 100
	mv *.eps plots/
	mv *.pdf plots/
	mv *.png plots/
	./convertPdfToEps.sh plots/
	okular plots/*.eps
