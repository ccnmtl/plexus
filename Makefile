APP=plexus

JS_FILES=media/js/makegraphs.js media/js/smoketests.js

VE=./ve
MANAGE=./manage.py
FLAKE8=$(VE)/bin/flake8


jenkins: $(VE)/bin/python check test flake8 jshint jscs

$(VE)/bin/python: requirements.txt bootstrap.py virtualenv.py
	./bootstrap.py

test: $(VE)/bin/python
	$(MANAGE) jenkins --pep8-exclude=migrations --enable-coverage --coverage-rcfile=.coveragerc

flake8: $(VE)/bin/python
	$(FLAKE8) $(APP) --max-complexity=8

runserver: $(VE)/bin/python check
	$(MANAGE) runserver

migrate: $(VE)/bin/python check jenkins
	$(MANAGE) migrate

check: $(VE)/bin/python
	$(MANAGE) check

shell: $(VE)/bin/python
	$(MANAGE) shell_plus

jshint: node_modules/jshint/bin/jshint
	./node_modules/jshint/bin/jshint $(JS_FILES)

jscs: node_modules/jscs/bin/jscs
	./node_modules/jscs/bin/jscs $(JS_FILES)

node_modules/jshint/bin/jshint:
	npm install jshint --prefix .

node_modules/jscs/bin/jscs:
	npm install jscs --prefix .

clean:
	rm -rf ve
	rm -rf media/CACHE
	rm -rf reports
	rm celerybeat-schedule
	rm .coverage
	find . -name '*.pyc' -exec rm {} \;

pull:
	git pull
	make check
	make test
	make migrate
	make flake8

rebase:
	git pull --rebase
	make check
	make test
	make migrate
	make flake8

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: $(VE)/bin/python check jenkins
	createdb $(APP)
	$(MANAGE) syncdb --noinput
	make migrate

# Docker related stuff
# use wheelhouse/requirements.txt as the sentinal so make
# knows whether it needs to rebuild the wheel directory or not
# has the added advantage that it can just pip install
# from that later on as well

ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

wheelhouse/requirements.txt: requirements.txt
	mkdir -p wheelhouse
	docker run --rm \
	-v $(ROOT_DIR):/app \
	-v $(ROOT_DIR)/wheelhouse:/wheelhouse \
	ccnmtl/django.build
	cp requirements.txt wheelhouse/requirements.txt
	touch wheelhouse/requirements.txt

build: wheelhouse/requirements.txt
	docker build -t ccnmtl/$(APP) .
