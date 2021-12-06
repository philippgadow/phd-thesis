monoWZ:
	lualatex monoWZ.tex
	rm *.aux *.log
	pdfcrop monoWZ.pdf
	mv monoWZ-crop.pdf monoWZ.pdf
clean:
	rm *.pdf *.aux *.log *.eps

.PHONY: monoWZ
