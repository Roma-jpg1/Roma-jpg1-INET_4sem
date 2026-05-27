PROJECT = main

.PHONY: all pdf clean fullclean

all: pdf

pdf:
	export LC_ALL=en_US.UTF-8; export LANG=en_US.UTF-8; latexmk -xelatex -synctex=1 -interaction=nonstopmode -file-line-error $(PROJECT).tex

# Ручная сборка, если не установлен latexmk
manual:
	export LC_ALL=en_US.UTF-8; export LANG=en_US.UTF-8; xelatex $(PROJECT).tex
	export LC_ALL=en_US.UTF-8; export LANG=en_US.UTF-8; biber $(PROJECT)
	export LC_ALL=en_US.UTF-8; export LANG=en_US.UTF-8; xelatex $(PROJECT).tex
	export LC_ALL=en_US.UTF-8; export LANG=en_US.UTF-8; xelatex $(PROJECT).tex

clean:
	latexmk -c
	rm -f *.bbl *.bcf *.run.xml *.nav *.snm *.vrb chapters/*.aux

fullclean: clean
	latexmk -C
	rm -f $(PROJECT).pdf
