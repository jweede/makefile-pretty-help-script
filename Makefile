SHELL := bash

#### Usage ####

## : default target is help
.PHONY: default
default: help

.PHONY: help # this help text
help:
	@# has no deps, should work with py2/py3
	@python makefile_self_document.py $(MAKEFILE_LIST)

.PHONY: fmt  # auto-format with black
fmt:
	black .

