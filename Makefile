file = my-thesis
make:
	 	# Run LaTeX the save way
		@pdflatex $(file)
		@biber $(file)
		@pdflatex $(file)
		# Reduce size of pdf
		@gs -sDEVICE=pdfwrite \
		    -dCompatibilityLevel=1.4 \
			-dNOPAUSE \
			-dQUIET \
			-dBATCH \
			-sOutputFile=$(file)_tmp.pdf \
			$(file).pdf
		@ rm $(file)_tmp.pdf
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol

one:
		# Run LaTeX just once
		@pdflatex $(file)

clean:
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol


ch01_file = ch01_introduction
ch01:
		@pdflatex chapters/$(ch01_file)
		@mv $(ch01_file).bcf chapters/
		@biber chapters/$(ch01_file)
		@mv chapters/$(ch01_file).b* .
		@pdflatex chapters/$(ch01_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol

ch01_draft_file = ch01_draft_introduction
ch01_draft:
		@pdflatex chapters/$(ch01_draft_file)
		@mv $(ch01_draft_file).bcf chapters/
		@biber chapters/$(ch01_draft_file)
		@mv chapters/$(ch01_draft_file).b* .
		@pdflatex chapters/$(ch01_draft_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol


ch02_file = ch02_standardmodel
ch02:
		@pdflatex chapters/$(ch02_file)
		@mv $(ch02_file).bcf chapters/
		@biber chapters/$(ch02_file)
		@mv chapters/$(ch02_file).b* .
		@pdflatex chapters/$(ch02_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol

ch02_draft_file = ch02_draft_standardmodel
ch02_draft:
		@pdflatex chapters/$(ch02_draft_file)
		@mv $(ch02_draft_file).bcf chapters/
		@biber chapters/$(ch02_draft_file)
		@mv chapters/$(ch02_draft_file).b* .
		@pdflatex chapters/$(ch02_draft_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol


ch03_file = ch03_darkmatter
ch03:
		@pdflatex chapters/$(ch03_file)
		@mv $(ch03_file).bcf chapters/
		@biber chapters/$(ch03_file)
		@mv chapters/$(ch03_file).b* .
		@pdflatex chapters/$(ch03_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol

ch03_draft_file = ch03_draft_darkmatter
ch03_draft:
		@pdflatex chapters/$(ch03_draft_file)
		@mv $(ch03_draft_file).bcf chapters/
		@biber chapters/$(ch03_draft_file)
		@mv chapters/$(ch03_draft_file).b* .
		@pdflatex chapters/$(ch03_draft_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol

ch04_file = ch04_protoncollisions
ch04:
		@pdflatex chapters/$(ch04_file)
		@mv $(ch04_file).bcf chapters/
		@biber chapters/$(ch04_file)
		@mv chapters/$(ch04_file).b* .
		@pdflatex chapters/$(ch04_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol

ch04_draft_file = ch04_draft_protoncollisions
ch04_draft:
		@pdflatex chapters/$(ch04_draft_file)
		@mv $(ch04_draft_file).bcf chapters/
		@biber chapters/$(ch04_draft_file)
		@mv chapters/$(ch04_draft_file).b* .
		@pdflatex chapters/$(ch04_draft_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol

ch05_file = ch05_detector
ch05:
		@pdflatex chapters/$(ch05_file)
		@mv $(ch05_file).bcf chapters/
		@biber chapters/$(ch05_file)
		@mv chapters/$(ch05_file).b* .
		@pdflatex chapters/$(ch05_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol

ch05_draft_file = ch05_draft_detector
ch05_draft:
		@pdflatex chapters/$(ch05_draft_file)
		@mv $(ch05_draft_file).bcf chapters/
		@biber chapters/$(ch05_draft_file)
		@mv chapters/$(ch05_draft_file).b* .
		@pdflatex chapters/$(ch05_draft_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol

ch06_file = ch06_trigger
ch06:
		@pdflatex chapters/$(ch06_file)
		@mv $(ch06_file).bcf chapters/
		@biber chapters/$(ch06_file)
		@mv chapters/$(ch06_file).b* .
		@pdflatex chapters/$(ch06_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol

ch06_draft_file = ch06_draft_trigger
ch06_draft:
		@pdflatex chapters/$(ch06_draft_file)
		@mv $(ch06_draft_file).bcf chapters/
		@biber chapters/$(ch06_draft_file)
		@mv chapters/$(ch06_draft_file).b* .
		@pdflatex chapters/$(ch06_draft_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol

ch07_file = ch07_methods
ch07:
		@pdflatex chapters/$(ch07_file)
		@mv $(ch07_file).bcf chapters/
		@biber chapters/$(ch07_file)
		@mv chapters/$(ch07_file).b* .
		@pdflatex chapters/$(ch07_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol


ch08_file = ch08_monoV
ch08:
		@pdflatex chapters/$(ch08_file)
		@mv $(ch08_file).bcf chapters/
		@biber chapters/$(ch08_file)
		@mv chapters/$(ch08_file).b* .
		@pdflatex chapters/$(ch08_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol

ch08_draft_file = ch08_draft_monoV
ch08_draft:
		@pdflatex chapters/$(ch08_draft_file)
		@mv $(ch08_draft_file).bcf chapters/
		@biber chapters/$(ch08_draft_file)
		@mv chapters/$(ch08_draft_file).b* .
		@pdflatex chapters/$(ch08_draft_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol


ch09_file = ch09_monoH
ch09:
		@pdflatex chapters/$(ch09_file)
		@mv $(ch09_file).bcf chapters/
		@biber chapters/$(ch09_file)
		@mv chapters/$(ch09_file).b* .
		@pdflatex chapters/$(ch09_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol

ch09_draft_file = ch09_draft_monoH
ch09_draft:
		@pdflatex chapters/$(ch09_draft_file)
		@mv $(ch09_draft_file).bcf chapters/
		@biber chapters/$(ch09_draft_file)
		@mv chapters/$(ch09_draft_file).b* .
		@pdflatex chapters/$(ch09_draft_file)
		@rm *aux *out *log *blg *bcf *bbl *xml  *toc *lof *lot *lol
		@rm chapters/*aux chapters/*out chapters/*log chapters/*blg chapters/*bcf chapters/*bbl chapters/*xml  chapters/*toc chapters/*lof chapters/*lot chapters/*lol


chapters: ch01 ch01_draft ch02 ch02_draft ch03 ch03_draft ch04 ch04_draft ch05 ch05_draft ch06 ch06_draft