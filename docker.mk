# Docker related stuff
# use wheelhouse/requirements.txt as the sentinal so make
# knows whether it needs to rebuild the wheel directory or not
# has the added advantage that it can just pip install
# from that later on as well

ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
WHEELHOUSE ?= wheelhouse
ORG ?= ccnmtl

$(WHEELHOUSE)/requirements.txt: $(REQUIREMENTS)
	mkdir -p $(WHEELHOUSE)
	docker run --rm \
	-v $(ROOT_DIR):/app \
	-v $(ROOT_DIR)/$(WHEELHOUSE):/wheelhouse \
	ccnmtl/django.build
	cp $(REQUIREMENTS) $(WHEELHOUSE)/requirements.txt
	touch $(WHEELHOUSE)/requirements.txt

build: $(WHEELHOUSE)/requirements.txt
	docker build -t $(ORG)/$(APP) .
