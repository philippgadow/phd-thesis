.PHONY: LO NLO

LO:
	mkdir -p plots
	python prettyLimitPlot.py data/dmVVhadInterpNewmu2D_95CL_obs.root -e -r data/relic-density/graphs/relic_V1.root -o monoV95CLsExpLimitPlot
	python prettyLimitPlot.py data/dmVVhadInterpNewmu2D_95CL_obs.root -e -r data/relic-density/graphs/relic_V1.root -o monoV95CLsExpLimitPlot_fancy --fancyRelicDensity
	python prettyLimitPlot.py data/dmVVhadInterpNewmu2D_95CL_obs.root -r data/relic-density/graphs/relic_V1.root
	python prettyLimitPlot.py data/dmVVhadInterpNewmu2D_95CL_obs.root -r data/relic-density/graphs/relic_V1.root -o monoV95CLsLimitPlot_fancy --fancyRelicDensity
	python prettyLimitPlot.py data/dmVVhadInterpNewmu2D_95CL_obs.root -o monoV95CLsLimitPlot_noRelicDensity

	python prettyLimitPlot.py data/dmVWhadInterpNewmu2D_95CL_obs.root -e -r data/relic-density/graphs/relic_V1.root -o monoW95CLsExpLimitPlot
	python prettyLimitPlot.py data/dmVWhadInterpNewmu2D_95CL_obs.root -e -r data/relic-density/graphs/relic_V1.root -o monoW95CLsExpLimitPlot_fancy --fancyRelicDensity
	python prettyLimitPlot.py data/dmVWhadInterpNewmu2D_95CL_obs.root -r data/relic-density/graphs/relic_V1.root -o monoW95CLsLimitPlot
	python prettyLimitPlot.py data/dmVWhadInterpNewmu2D_95CL_obs.root -r data/relic-density/graphs/relic_V1.root -o monoW95CLsLimitPlot_fancy --fancyRelicDensity
	python prettyLimitPlot.py data/dmVWhadInterpNewmu2D_95CL_obs.root -o monoW95CLsLimitPlot_noRelicDensity

	python prettyLimitPlot.py data/dmVZhadInterpNewmu2D_95CL_obs.root -e -r data/relic-density/graphs/relic_V1.root -o monoZ95CLsExpLimitPlot
	python prettyLimitPlot.py data/dmVZhadInterpNewmu2D_95CL_obs.root -e -r data/relic-density/graphs/relic_V1.root -o monoZ95CLsExpLimitPlot_fancy --fancyRelicDensity
	python prettyLimitPlot.py data/dmVZhadInterpNewmu2D_95CL_obs.root -r data/relic-density/graphs/relic_V1.root -o monoZ95CLsLimitPlot
	python prettyLimitPlot.py data/dmVZhadInterpNewmu2D_95CL_obs.root -r data/relic-density/graphs/relic_V1.root -o monoZ95CLsLimitPlot_fancy --fancyRelicDensity
	python prettyLimitPlot.py data/dmVZhadInterpNewmu2D_95CL_obs.root -o monoZ95CLsLimitPlot_noRelicDensity

	mv *.eps plots/
	mv *.pdf plots/
	mv *.png plots/
	# ./convertPdfToEps.sh plots/
	okular plots/*.eps

NLO:
	mkdir -p plots_nlo
	python prettyLimitPlot.py data_nlo-2018-04-04/dmV1VhadInterp3newNewmu2D_obs.root -e -r data/relic-density/graphs/relic_V1.root -o monoVV195CLsExpLimitPlot -t "Mono-V(qq): Vector, Dirac" --textNLO "(NLO)"
	python prettyLimitPlot.py data_nlo-2018-04-04/dmV1WhadInterp3newNewmu2D_obs.root -e -r data/relic-density/graphs/relic_V1.root -o monoWV195CLsExpLimitPlot -t "Mono-W(qq): Vector, Dirac" --textNLO "(NLO)"
	python prettyLimitPlot.py data_nlo-2018-04-04/dmV1ZhadInterp3newNewmu2D_obs.root -e -r data/relic-density/graphs/relic_V1.root -o monoZV195CLsExpLimitPlot -t "Mono-Z(qq): Vector, Dirac" --textNLO "(NLO)"

	python prettyLimitPlot.py data_nlo-2018-04-04/dmV1VhadInterp3newNewmu2D_obs.root -r data/relic-density/graphs/relic_V1.root -o monoVV195CLsLimitPlot -t "Mono-V(qq): Vector, Dirac" --textNLO "(NLO)"
	python prettyLimitPlot.py data_nlo-2018-04-04/dmV1WhadInterp3newNewmu2D_obs.root -r data/relic-density/graphs/relic_V1.root -o monoWV195CLsLimitPlot -t "Mono-W(qq): Vector, Dirac" --textNLO "(NLO)"
	python prettyLimitPlot.py data_nlo-2018-04-04/dmV1ZhadInterp3newNewmu2D_obs.root -r data/relic-density/graphs/relic_V1.root -o monoZV195CLsLimitPlot -t "Mono-Z(qq): Vector, Dirac" --textNLO "(NLO)"

	python prettyLimitPlot.py data_nlo-2018-04-04/dmA1VhadInterp3newNewmu2D_obs.root -e -r data/relic-density/graphs/relic_A1.root -o monoVA195CLsExpLimitPlot -t "Mono-V(qq): Axial-Vector, Dirac" --textNLO "(NLO)"
	python prettyLimitPlot.py data_nlo-2018-04-04/dmA1WhadInterp3newNewmu2D_obs.root -e -r data/relic-density/graphs/relic_A1.root -o monoWA195CLsExpLimitPlot -t "Mono-W(qq): Axial-Vector, Dirac" --textNLO "(NLO)"
	python prettyLimitPlot.py data_nlo-2018-04-04/dmA1ZhadInterp3newNewmu2D_obs.root -e -r data/relic-density/graphs/relic_A1.root -o monoZA195CLsExpLimitPlot -t "Mono-Z(qq): Axial-Vector, Dirac" --textNLO "(NLO)"

	python prettyLimitPlot.py data_nlo-2018-04-04/dmA1VhadInterp3newNewmu2D_obs.root -r data/relic-density/graphs/relic_A1.root -o monoVA195CLsLimitPlot -t "Mono-V(qq): Axial-Vector, Dirac" --textNLO "(NLO)"
	python prettyLimitPlot.py data_nlo-2018-04-04/dmA1WhadInterp3newNewmu2D_obs.root -r data/relic-density/graphs/relic_A1.root -o monoWA195CLsLimitPlot -t "Mono-W(qq): Axial-Vector, Dirac" --textNLO "(NLO)"
	python prettyLimitPlot.py data_nlo-2018-04-04/dmA1ZhadInterp3newNewmu2D_obs.root -r data/relic-density/graphs/relic_A1.root -o monoZA195CLsLimitPlot -t "Mono-Z(qq): Axial-Vector, Dirac" --textNLO "(NLO)"

	mv *.eps plots_nlo/
	mv *.pdf plots_nlo/
	mv *.png plots_nlo/
	# ./convertPdfToEps.sh plots_nlo/
	okular plots_nlo/*.eps
