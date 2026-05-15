WEEK ?= 01
PYTHON ?= python3

.PHONY: test

test:
	$(PYTHON) -m pytest -q weeks/week-$(WEEK)/tests
