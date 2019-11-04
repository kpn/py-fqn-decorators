# This Makefile requires the following commands to be available:
# * python3.6
# * docker
# * docker-compose

DEPS:=requirements.txt
DOCKER_COMPOSE:=$(shell which docker-compose)

PIP:="venv/bin/pip"
CMD_FROM_VENV:=". venv/bin/activate; which"
TOX=$(shell "$(CMD_FROM_VENV)" "tox")
PYTHON=$(shell "$(CMD_FROM_VENV)" "python")
TWINE=$(shell "$(CMD_FROM_VENV)" "twine")
TOX_PY_LIST="$(shell $(TOX) -l | grep ^py | xargs | sed -e 's/ /,/g')"

.PHONY: clean pyclean test lint isort docker setup.py build publish

tox:
	$(TOX)

pyclean:
	@find . -name *.pyc -delete
	@rm -rf *.egg-info build
	@rm -rf coverage.xml .coverage

clean: pyclean
	@rm -rf venv
	@rm -rf .tox

venv:
	@python3.6 -m venv venv
	@$(PIP) install -U "pip>=7.0" -q
	@$(PIP) install -U setuptools -q
	@$(PIP) install -r $(DEPS)

test: venv pyclean
	$(TOX) -e $(TOX_PY_LIST)

test/%: venv pyclean
	$(TOX) -e $(TOX_PY_LIST) -- $*

lint: venv
	@$(TOX) -e lint
	@$(TOX) -e isort-check

isort: venv
	@$(TOX) -e isort-fix

docker:
	$(DOCKER_COMPOSE) run --rm --service-ports app bash

docker/%:
	$(DOCKER_COMPOSE) run --rm --service-ports app make $*

## Distribution
setup.py: venv
	@$(PYTHON) setup_gen.py

build: venv tox
	-rm -f setup.py
	-rm -rf dist build
	$(MAKE) setup.py
	$(PYTHON) setup.py sdist
	$(TWINE) check dist/*

publish: build
	$(TWINE) upload dist/*
