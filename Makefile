.PHONY: clean data lint requirements bootstrap

SHELL := /bin/bash

#################################################################################
# COMMANDS                                                                      #
#################################################################################

bootstrap:
	( \
	source `which virtualenvwrapper.sh`; \
	mkvirtualenv -p /home/molhaem2/rbeagrie/.local/ActivePython-3.5/bin/python3 oudelaar-tiled-capture-2019; \
	)
	git init
	echo "*.ipynb filter=ipynb_stripout" >> .gitattributes
	git add .gitattributes
	git commit -m "Added ipynb_stripout. See https://github.com/jond3k/ipynb_stripout" .gitattributes


requirements:
	( \
	source `which virtualenvwrapper.sh`; \
	deactivate; \
	workon oudelaar-tiled-capture-2019; \
	pip install --upgrade pip; \
	ulimit -s 8024; \
	pip install -r requirements.txt; \
	)

data: requirements
	python src/data/make_dataset.py

clean:
	find . -name "*.pyc" -exec rm {} \;

lint:
	flake8 --exclude=lib/,bin/ .

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################
